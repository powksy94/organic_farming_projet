from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from data.database import get_db
from model.models import Plot, Crop, Observation, Alert, Weather

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):
    total_plots = db.query(Plot).count()
    total_area = db.query(func.sum(Plot.area_ha)).scalar() or 0

    crops_by_type = dict(
        db.query(Crop.type, func.count(Crop.id))
        .group_by(Crop.type).all()
    )

    active_alerts = db.query(Alert).filter(Alert.resolved == False).count()
    critical_alerts = (
        db.query(Alert)
        .filter(Alert.resolved == False, Alert.level == 3)
        .count()
    )

    observation_states = dict(
        db.query(Observation.state, func.count(Observation.id))
        .group_by(Observation.state).all()
    )

    recent_observations = (
        db.query(Observation).order_by(Observation.date.desc()).limit(5).all()
    )

    latest_weather = db.query(Weather).order_by(Weather.date.desc()).first()

    return {
        "plots": {
            "total": total_plots,
            "total_area_ha": round(total_area, 2),
        },
        "crops": crops_by_type,
        "alerts": {
            "active": active_alerts,
            "critical": critical_alerts,
        },
        "observations": {
            "states": observation_states,
            "recent": [
                {
                    "id": o.id,
                    "date": str(o.date),
                    "state": o.state,
                    "plot_id": o.plot_id,
                    "comment": o.comment,
                }
                for o in recent_observations
            ],
        },
        "latest_weather": {
            "date": str(latest_weather.date),
            "temperature": latest_weather.temperature,
            "humidity": latest_weather.humidity,
            "rain_mm": latest_weather.rain_mm,
        } if latest_weather else None,
    }