import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.database import get_db
from schemas.appointment import AppointmentCreate, AppointmentUpdate

router = APIRouter()

@router.get("/")
def list_appointments(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name,
               d.specialization, h.name AS hospital_name, h.city,
               a.appointment_date, a.status, a.notes
        FROM Appointments a
        JOIN Patients p ON a.patient_id = p.patient_id
        JOIN Doctors d ON a.doctor_id = d.doctor_id
        JOIN Hospitals h ON a.hospital_id = h.hospital_id
        ORDER BY a.appointment_date DESC
    """))
    return {"appointments": [dict(r) for r in result.mappings().all()]}

@router.get("/doctors")
def list_doctors(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT d.doctor_id, d.name, d.specialization, h.name AS hospital_name
        FROM Doctors d JOIN Hospitals h ON d.hospital_id = h.hospital_id
        ORDER BY d.name
    """))
    return {"doctors": [dict(r) for r in result.mappings().all()]}

@router.get("/hospitals")
def list_hospitals(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT hospital_id, name, city, state FROM Hospitals ORDER BY name"))
    return {"hospitals": [dict(r) for r in result.mappings().all()]}

@router.post("/", status_code=201)
def create_appointment(body: AppointmentCreate, db: Session = Depends(get_db)):
    aid = str(uuid.uuid4())
    db.execute(text("""
        INSERT INTO Appointments (appointment_id, patient_id, doctor_id, hospital_id, appointment_date, notes)
        VALUES (:aid, :patient_id, :doctor_id, :hospital_id, :appointment_date, :notes)
    """), {"aid": aid, "patient_id": body.patient_id, "doctor_id": body.doctor_id,
           "hospital_id": body.hospital_id, "appointment_date": body.appointment_date,
           "notes": body.notes})
    db.commit()
    return {"message": "Appointment booked", "appointment_id": aid}

@router.put("/{appointment_id}")
def update_appointment(appointment_id: str, body: AppointmentUpdate, db: Session = Depends(get_db)):
    fields = {k: v for k, v in body.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["aid"] = appointment_id
    result = db.execute(text(f"UPDATE Appointments SET {set_clause} WHERE appointment_id = :aid"), fields)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment updated"}

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: str, db: Session = Depends(get_db)):
    result = db.execute(text("DELETE FROM Appointments WHERE appointment_id = :aid"), {"aid": appointment_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted"}