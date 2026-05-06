from sqlalchemy.orm import Session
from datetime import date
from model.models import Weather, Observation, Alert, Plot

HUMIDITY_DISEASE_THRESHOLD = 80
TEMP_DISEASE_THRESHOLD = 20
DRY_DAYS_THRESHOLD = 3

def generate_alerts(db: Session, plot_id: int = None) -> list:
    plots = db.query(Plot).all()
    if plot_id is not None:
        plots = [p for p in plots if p.id == plot_id]

    recent_weather = db.query(Weather).order_by(Weather.date.desc()).limit(7).all()
    new_alerts = []

    for plot in plots:
        new_alerts += _rule_disease_risk(db, plot, recent_weather)
        new_alerts += _rule_water_stress(db, plot, recent_weather)
        new_alerts += _rule_observed_disease(db, plot)

    for alert in new_alerts:
        db.add(alert)
    db.commit()
    for alert in new_alerts:
        db.refresh(alert)
    return new_alerts

def _rule_disease_risk(db, plot, recent_weather) -> list:
    for w in recent_weather:
        if w.humidity > HUMIDITY_DISEASE_THRESHOLD and w.temperature > TEMP_DISEASE_THRESHOLD:
            if _alert_exists(db, plot.id, "Risque maladie", w.date):
                return []
            level = 3 if w.humidity > 90 else 2
            return [Alert(
                date=w.date,
                type="Risque maladie",
                plot_id=plot.id,
                level=level,
            )]
    return []
    
def _rule_water_stress(db, plot, recent_weather) -> list:
    dry_days = sum(1 for w in recent_weather if w.rain_mm == 0)
    if dry_days < DRY_DAYS_THRESHOLD:
        return []
    today = date.today()
    if _alert_exists(db, plot.id, "Stress hydrique", today):
        return []
    level = min(max(dry_days // 2, 1), 3)
    return [Alert(
        date=today,
        type="Stress hydrique",
        plot_id=plot.id,
        level=level,
    )]

def _rule_observed_disease(db, plot) -> list:
    obs = (
        db.query(Observation)
        .filter(
            Observation.plot_id == plot.id,
            Observation.state == "Maladie détectée",
        )
        .order_by(Observation.date.desc())
        .first()
    )
    if not obs or _alert_exists(db, plot.id, "Risque maladie", obs.date):
        return []
    return [Alert(
        date=obs.date,
        type="Risque maladie",
        plot_id=plot.id,
        level=3,
    )]

def _alert_exists(db: Session, plot_id: int, type_: str, date_: date) -> bool:
    return db.query(Alert).filter(
        Alert.plot_id == plot_id,
        Alert.type == type_,
        Alert.date == date_,
        Alert.resolved == False,
    ).first() is not None
