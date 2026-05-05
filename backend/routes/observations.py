from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Observation
from schemas import ObservationCreate, ObservationRead

router = APIRouter(prefix="/observations", tags=["Observations"])

@router.get("/", response_model=List[ObservationRead])
def get_all(plot_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Observation)
    if plot_id:
        query = query.filter(Observation.plot_id == plot_id)
    return query.order_by(Observation.date.desc()).all()

@router.get("/{id}", response_model=ObservationRead)
def get_one(id: int, db: Session = Depends(get_db)):
    obs = db.get(Observation, id)
    if not obs:
        raise HTTPException(404, "Observation not found")
    return obs


@router.post("/", response_model=ObservationRead, status_code=201)
def create(data: ObservationCreate, db: Session = Depends(get_db)):
    obs = Observation(**data.model_dump())
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs

@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    obs = db.get(Observation, id)
    if not obs:
        raise HTTPException(404, "Observation not found")
    db.delete(obs)
    db.commit()
