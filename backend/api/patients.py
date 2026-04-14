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