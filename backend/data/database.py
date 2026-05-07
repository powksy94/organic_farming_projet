from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import csv
import os
from datetime import date

DATABASE_URL = "sqlite:///./agriculture.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from model.models import Plot, Crop, Observation, Alert, Weather
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Plot).count() == 0:
            _seed_from_csv(db)
    finally:
        db.close()

def _seed_from_csv(db):
    from model.models import Plot, Crop, Observation, Alert, Weather
    dataset_dir = os.path.join(os.path.dirname(__file__), "..", "dataset_agriculture (2)")

    with open(os.path.join(dataset_dir, "parcelles.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            db.add(Plot(
                id=int(row["id"]),
                name=row["nom"],
                location=row["localisation"],
                area_ha=float(row["surface_ha"])
            ))
    
    with open(os.path.join(dataset_dir, "cultures.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            db.add(Crop(
                id=int(row["id"]),
                type=row["type"],
                planting_date=date.fromisoformat(row["date_semis"]),
                plot_id=int(row["parcelle_id"])
            ))

    with open(os.path.join(dataset_dir, "observations.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            db.add(Observation(
                date=date.fromisoformat(row["date"]),
                state=row["etat"],
                plot_id=int(row["parcelle_id"]),
                comment=row["commentaire"]
            ))

    with open(os.path.join(dataset_dir, "alertes.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            db.add(Alert(
                date=date.fromisoformat(row["date"]),
                type=row["type"],
                plot_id=int(row["parcelle_id"]),
                level=int(row["niveau"])
            ))

    with open(os.path.join(dataset_dir, "meteo.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            db.add(Weather(
                date=date.fromisoformat(row["date"]),
                temperature=float(row["temperature"]),
                humidity=float(row["humidite"]),
                rain_mm=float(row["pluie_mm"])
            ))
    
    db.commit()
