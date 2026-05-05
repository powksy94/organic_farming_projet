from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Plot
from schemas import PlotCreate, PlotRead

router = APIRouter(prefix="/plots", tags=["Plots"])

@router.get("/", response_model=List[PlotRead])
def get_all(db: Session = Depends(get_db)):
    return db.query(Plot).all()

@router.get("/{id}", response_model=PlotRead)
def get_one(id: int, db: Session = Depends(get_db)):
    plot = db.get(Plot, id)
    if not plot:
        raise HTTPException(404, "Plot not found")
    return plot

@router.post("/", response_model=PlotRead, status_code=201)
def create(data: PlotCreate, db: Session = Depends(get_db)):
    plot = Plot(**data.model_dump())
    db.add(plot)
    db.commit()
    db.refresh(plot)
    return plot

@router.put("/{id}", response_model=PlotRead)
def update(id: int, data: PlotCreate, db: Session = Depends(get_db)):
    plot = db.get(Plot, id)
    if not plot:
        raise HTTPException(404, "Plot not found")
    for key, value in data.model_dump().items():
        setattr(plot, key, value)
    db.commit()
    db.refresh(plot)
    return plot

@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    plot = db.get(Plot, id)
    if not plot:
        raise HTTPException(404, "Plot not found")
    db.delete(plot)
    db.commit()