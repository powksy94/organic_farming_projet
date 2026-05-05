from pydantic import BaseModel
from datetime import date
from typing import Optional

class PlotBase(BaseModel):
    name: str
    location: str
    area_ha: float

class PlotCreate(PlotBase):
    pass

class PlotRead(PlotBase):
    id: int 
    class Config:
        from_attributes = True

class CropBase(BaseModel):
    type: str
    planting_date: date
    plot_id: int

class CropCreate(CropBase):
    pass

class CropRead(CropBase):
    id: int
    class Config:
        from_attributes = True

class ObservationBase(BaseModel):
    date: date
    state: str
    plot_id: int
    comment: Optional[str] = None

class ObservationCreate(ObservationBase):
    pass

class ObservationRead(ObservationBase):
    id: int
    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    date: date
    type: str
    plot_id: int
    level: int

class AlertCreate(AlertBase):
    pass

class AlertRead(AlertBase):
    id: int
    resolved: bool
    class Config:
        from_attributes = True

class WeatherBase(BaseModel):
    date: date
    temperature: float
    humidity: float
    rain_mm: float

class WeatherCreate(WeatherBase):
    pass

class WeatherRead(WeatherBase):
    id: int
    class Config:
        from_attributes = True