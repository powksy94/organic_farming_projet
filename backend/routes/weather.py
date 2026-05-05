from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from database import get_db
from models import Weather
from schemas import WeatherCreate, WeatherRead

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/", response_model=List[WeatherRead])
def get_all(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Weather)
    if start_date:
        query = query.filter(Weather.date >= start_date)
    if end_date:
        query = query.filter(Weather.date <= end_date)
    return query.order_by(Weather.date.desc()).all()

@router.post("/", response_model=WeatherRead, status_code=201)
def create(data: WeatherCreate, db: Session = Depends(get_db)):
    if db.query(Weather).filter(Weather.date == data.date).first():
        raise HTTPException(400, "Weather entry already exists for this date")
    entry = Weather(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry