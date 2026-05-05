from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import plots, crops, observations, alerts, weather, dashboard

app = FastAPI(title="Agriculture API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(dashboard.router, prefix="/api")
app.include_router(plots.router, prefix="/api")
app.include_router(crops.router, prefix="/api")
app.include_router(observations.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(weather.router, prefix="/api")