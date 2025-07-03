from fastapi import FastAPI, HTTPException, Depends, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import UUID
import asyncio

import models
import schemas
import crud
import database
import ws_manager


app = FastAPI(title="ORo Robot Telemetry Dashboard", openapi_url="/openapi.json")

# Serve static files like CSS and JS
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Template engine setup for HTML
templates = Jinja2Templates(directory="frontend")

# Show dashboard on homepage
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/devices/", response_model=schemas.RobotDevice)
async def create_device(device: schemas.RobotDeviceCreate, db: Session = Depends(get_db)):
    return crud.create_device(db, device)

@app.get("/devices/", response_model=list[schemas.RobotDevice])
async def list_devices(db: Session = Depends(get_db)):
    return crud.get_devices(db)

@app.post("/metrics/types/", response_model=schemas.TelemetryMetric)
async def create_metric_type(metric: schemas.TelemetryMetricCreate, db: Session = Depends(get_db)):
    return crud.create_metric_type(db, metric)

@app.post("/metrics/{device_id}/data/", response_model=schemas.TelemetryData)
async def create_telemetry_data(device_id: UUID, data: schemas.TelemetryDataCreate, db: Session = Depends(get_db)):
    return crud.create_telemetry_data(db, device_id, data)

@app.get("/metrics/{device_id}/data/", response_model=list[schemas.TelemetryData])
async def get_telemetry_data(device_id: UUID, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_telemetry_data(db, device_id, limit)

@app.get("/metrics/{device_id}/summary/", response_model=dict)
async def get_telemetry_summary(device_id: UUID, db: Session = Depends(get_db)):
    return crud.get_telemetry_summary(db, device_id)

@app.post("/commands/{device_id}/", response_model=schemas.CommandLog)
async def send_command(device_id: UUID, command: schemas.CommandLogCreate, db: Session = Depends(get_db)):
    return crud.create_command_log(db, device_id, command)

@app.get("/commands/{device_id}/", response_model=list[schemas.CommandLog])
async def get_command_logs(device_id: UUID, limit: int = 5, db: Session = Depends(get_db)):
    return crud.get_command_logs(db, device_id, limit)

@app.websocket("/ws/telemetry/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: UUID, db: Session = Depends(get_db)):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = crud.get_latest_telemetry(db, device_id)
            await ws_manager.send_personal_message(data, websocket)
            await asyncio.sleep(2)
    except Exception:
        ws_manager.disconnect(websocket)

@app.get("/dashboard")
async def get_dashboard():
    with open("frontend/dashboard.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)