from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Crop
from schemas import CropCreate, CropRead

router = APIRouter(prefix="/crops", tags=["Crops"])

@router.get("/", response_model=List[CropRead])
def get_all(plot_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Crop)
    if plot_id:
        query = query.filter(Crop.plot_id == plot_id)
    return query.all()

@router.get("/{id}", response_model=CropRead)
def get_one(id: int, db: Session = Depends(get_db)):
    crop = db.get(Crop, id)
    if not crop:
        raise HTTPException(404, "Crop not found")
    return crop

@router.post("/", response_model=CropRead, status_code=201)
def create(data: CropCreate, db: Session = Depends(get_db)):
    crop = Crop(**data.model_dump())
    db.add(crop)
    db.commit()
    db.refresh(crop)
    return crop

@router.put("/{id}", response_model=CropRead)
def update(id: int, data: CropCreate, db: Session = Depends(get_db)):
    crop = db.get(Crop, id)
    if not crop:
        raise HTTPException(404, "Crop not found")
    for key, value in data.model_dump().items():
        setattr(crop, key, value)
    db.commit()
    db.refresh(crop)
    return crop

@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    crop = db.get(Crop, id)
    if not crop:
        raise HTTPException(404, "Crop not found")
    db.delete(crop)
    db.commit()