from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from data.database import Base

class Plot(Base):
    __tablename__ = "plots"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    area_ha = Column(Float)

class Crop(Base):
    __tablename__ = "crops"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    planting_date = Column(Date)
    plot_id = Column(Integer, ForeignKey("plots.id"), nullable=False)

class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    state = Column(String)
    plot_id = Column(Integer, ForeignKey("plots.id"), nullable=False)
    comment = Column(String)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    type = Column(String)
    plot_id = Column(Integer, ForeignKey("plots.id"), nullable=False)
    level = Column(Integer)
    resolved = Column(Boolean, default=False)

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    rain_mm = Column(Float)