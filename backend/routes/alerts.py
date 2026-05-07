from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from data.database import get_db
from model.models import Alert
from schemas import AlertRead
from services.alert_service import generate_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/", response_model=List[AlertRead])
def get_all(
    plot_id: Optional[int] = None,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Alert)
    if plot_id is not None:
        query = query.filter(Alert.plot_id == plot_id)
    if resolved is not None: 
        query = query.filter(Alert.resolved == resolved)
    return query.order_by(Alert.date.desc()).all()

@router.put("/{id}/resolve", response_model=AlertRead)
def resolve(id: int, db: Session = Depends(get_db)):
    alert = db.get(Alert, id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    alert.resolved = True
    db.commit()
    db.refresh(alert)
    return alert

@router.post("/generate", response_model=List[AlertRead])
def generate(plot_id: Optional[int] = None, db: Session = Depends(get_db)):
    return generate_alerts(db, plot_id)