import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.database import get_db
from db import queries
from schemas.patient import PatientCreate, PatientUpdate

router = APIRouter()

@router.get("/")
def list_patients(db: Session = Depends(get_db)):
    result = queries.get_all_patients(db)
    return {"patients": [dict(r) for r in result]}

@router.get("/high-risk/list")
def high_risk_patients(threshold: float = 70.0, db: Session = Depends(get_db)):
    result = queries.get_high_risk_patients(db, threshold)
    return {"threshold": threshold, "patients": [dict(r) for r in result]}

@router.get("/no-disease/list")
def patients_without_disease(db: Session = Depends(get_db)):
    result = queries.get_patients_without_disease(db)
    return {"patients": [dict(r) for r in result]}

@router.get("/{patient_id}/risk")
def patient_risk(patient_id: str, db: Session = Depends(get_db)):
    result = queries.get_patient_risk_score(db, patient_id)
    if not result:
        raise HTTPException(status_code=404, detail="Risk score not found")
    return dict(result)

@router.get("/{patient_id}/appointments")
def patient_appointments(patient_id: str, db: Session = Depends(get_db)):
    result = queries.get_patient_appointments(db, patient_id)
    return {"appointments": [dict(r) for r in result]}

@router.get("/{patient_id}/symptoms")
def patient_symptoms(patient_id: str, db: Session = Depends(get_db)):
    result = queries.get_patient_symptoms(db, patient_id)
    return {"symptoms": [dict(r) for r in result]}

@router.get("/{patient_id}/orders")
def patient_orders(patient_id: str, db: Session = Depends(get_db)):
    result = queries.get_patient_orders(db, patient_id)
    return {"orders": [dict(r) for r in result]}

@router.post("/", status_code=201)
def create_patient(body: PatientCreate, db: Session = Depends(get_db)):
    pid = str(uuid.uuid4())
    db.execute(text("""
        INSERT INTO Patients (patient_id, name, age, gender, blood_group, phone, email, address)
        VALUES (:pid, :name, :age, :gender, :blood_group, :phone, :email, :address)
    """), {"pid": pid, "name": body.name, "age": body.age,
           "gender": body.gender, "blood_group": body.blood_group,
           "phone": body.phone, "email": body.email, "address": body.address})
    db.commit()
    return {"message": "Patient created", "patient_id": pid}

@router.put("/{patient_id}")
def update_patient(patient_id: str, body: PatientUpdate, db: Session = Depends(get_db)):
    fields = {k: v for k, v in body.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["patient_id"] = patient_id
    result = db.execute(text(f"UPDATE Patients SET {set_clause} WHERE patient_id = :patient_id"), fields)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient updated"}

@router.delete("/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    result = db.execute(text("DELETE FROM Patients WHERE patient_id = :pid"), {"pid": patient_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted"}


# ── ASSIGN SYMPTOM ───────────────────────────────────────────
@router.post("/{patient_id}/symptoms")
def add_symptom(patient_id: str, body: dict, db: Session = Depends(get_db)):
    from sqlalchemy import text as t
    symptom_id = body.get("symptom_id")
    if not symptom_id:
        raise HTTPException(status_code=400, detail="symptom_id required")
    # check if already assigned
    exists = db.execute(t("""
        SELECT 1 FROM Patient_Symptoms
        WHERE patient_id = :pid AND symptom_id = :sid
    """), {"pid": patient_id, "sid": symptom_id}).first()
    if exists:
        raise HTTPException(status_code=400, detail="Symptom already recorded")
    db.execute(t("""
        INSERT INTO Patient_Symptoms (patient_id, symptom_id, reported_on)
        VALUES (:pid, :sid, CURDATE())
    """), {"pid": patient_id, "sid": symptom_id})
    db.commit()
    return {"message": "Symptom added"}


# ── SUBMIT HEALTH DATA + RISK SCORE ─────────────────────────
@router.post("/{patient_id}/health")
def submit_health(patient_id: str, body: dict, db: Session = Depends(get_db)):
    import uuid as _uuid
    from sqlalchemy import text as t

    rid = str(_uuid.uuid4())
    # Insert into Heart_Data with whatever fields are provided
    db.execute(t("""
        INSERT INTO Heart_Data
        (record_id, patient_id, age, sex, cp, trestbps, chol, fbs, thalach, target)
        VALUES (:rid, :pid, :age, :sex, :cp, :trestbps, :chol, :fbs, :thalach, :target)
    """), {
        "rid": rid,
        "pid": patient_id,
        "age":      body.get("age"),
        "sex":      body.get("sex", 1),
        "cp":       body.get("cp", 0),
        "trestbps": body.get("bp"),
        "chol":     body.get("chol"),
        "fbs":      1 if body.get("fbs", False) else 0,
        "thalach":  body.get("max_hr"),
        "target":   body.get("target", 0),
    })

    # Calculate simple risk scores based on input
    heart_s  = min(100, round(
        (30 if body.get("target", 0) == 1 else 0) +
        (20 if (body.get("chol") or 0) > 240 else 0) +
        (15 if (body.get("bp") or 0) > 140 else 0) +
        (10 if body.get("fbs") else 0), 2))

    cardio_s = min(100, round(
        (25 if (body.get("bp") or 0) > 140 else 0) +
        (20 if (body.get("chol") or 0) > 240 else 0) +
        (15 if body.get("smoke", False) else 0) +
        (10 if body.get("alco", False) else 0), 2))

    kidney_s = min(100, round(
        (30 if body.get("htn", False) else 0) +
        (25 if body.get("dm", False) else 0) +
        (15 if (body.get("bp") or 0) > 140 else 0), 2))

    overall = round((heart_s + cardio_s + kidney_s) / 3, 2)

    # Upsert risk score
    existing = db.execute(t(
        "SELECT score_id FROM Risk_Scores WHERE patient_id = :pid"),
        {"pid": patient_id}).first()

    if existing:
        db.execute(t("""
            UPDATE Risk_Scores
            SET heart_score=:hs, cardio_score=:cs, kidney_score=:ks, overall_score=:os
            WHERE patient_id=:pid
        """), {"hs": heart_s, "cs": cardio_s, "ks": kidney_s, "os": overall, "pid": patient_id})
    else:
        db.execute(t("""
            INSERT INTO Risk_Scores
            (score_id, patient_id, heart_score, cardio_score, kidney_score, overall_score)
            VALUES (:sid, :pid, :hs, :cs, :ks, :os)
        """), {"sid": str(_uuid.uuid4()), "pid": patient_id,
               "hs": heart_s, "cs": cardio_s, "ks": kidney_s, "os": overall})

    db.commit()
    return {"message": "Health data saved", "heart_score": heart_s,
            "cardio_score": cardio_s, "kidney_score": kidney_s, "overall_score": overall}