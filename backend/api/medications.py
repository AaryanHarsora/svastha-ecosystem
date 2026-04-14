import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.database import get_db
from db import queries
from schemas.medication import MedicationCreate, MedicationUpdate

router = APIRouter()

@router.get("/")
def list_medications(db: Session = Depends(get_db)):
    result = queries.get_all_medications(db)
    return {"medications": [dict(r) for r in result]}

@router.get("/top-selling")
def top_selling(limit: int = 5, db: Session = Depends(get_db)):
    result = queries.get_top_selling_medications(db, limit)
    return {"medications": [dict(r) for r in result]}

@router.get("/cheapest-per-category")
def cheapest_per_category(db: Session = Depends(get_db)):
    result = queries.get_cheapest_medicine_per_category(db)
    return {"medications": [dict(r) for r in result]}

@router.post("/", status_code=201)
def create_medication(body: MedicationCreate, db: Session = Depends(get_db)):
    mid = str(uuid.uuid4())
    db.execute(text("""
        INSERT INTO Medications (medication_id, name, generic_name, category, dosage_form, strength, description)
        VALUES (:mid, :name, :generic_name, :category, :dosage_form, :strength, :description)
    """), {"mid": mid, "name": body.name, "generic_name": body.generic_name,
           "category": body.category, "dosage_form": body.dosage_form,
           "strength": body.strength, "description": body.description})
    db.commit()
    return {"message": "Medication created", "medication_id": mid}

@router.put("/{medication_id}")
def update_medication(medication_id: str, body: MedicationUpdate, db: Session = Depends(get_db)):
    fields = {k: v for k, v in body.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["mid"] = medication_id
    result = db.execute(text(f"UPDATE Medications SET {set_clause} WHERE medication_id = :mid"), fields)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Medication not found")
    return {"message": "Medication updated"}

@router.delete("/{medication_id}")
def delete_medication(medication_id: str, db: Session = Depends(get_db)):
    result = db.execute(text("DELETE FROM Medications WHERE medication_id = :mid"), {"mid": medication_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Medication not found")
    return {"message": "Medication deleted"}