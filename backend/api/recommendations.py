from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import queries

router = APIRouter()


@router.get("/{patient_id}")
def get_recommendations(patient_id: str, db: Session = Depends(get_db)):
    result = queries.get_patient_recommendations(db, patient_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No recommendations found — patient may have no recorded diseases"
        )
    return {
        "patient_id": patient_id,
        "recommendations": [dict(r) for r in result]
    }