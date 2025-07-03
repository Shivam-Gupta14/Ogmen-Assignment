from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas
from fastapi import HTTPException
from uuid import UUID

def create_device(db: Session, device: schemas.RobotDeviceCreate):
    db_device = models.RobotDevice(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(db: Session):
    return db.query(models.RobotDevice).all()

def create_metric_type(db: Session, metric: schemas.TelemetryMetricCreate):
    db_metric = models.TelemetryMetric(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

def create_telemetry_data(db: Session, device_id: UUID, data: schemas.TelemetryDataCreate):
    metric = db.query(models.TelemetryMetric).filter(models.TelemetryMetric.metric_name == data.metric_name).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    db_data = models.TelemetryData(device_id=device_id, metric_id=metric.metric_id, value=data.value)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_telemetry_data(db: Session, device_id: UUID, limit: int):
    return db.query(models.TelemetryData).join(models.TelemetryMetric).filter(
        models.TelemetryData.device_id == device_id
    ).order_by(models.TelemetryData.recorded_at.desc()).limit(limit).all()

def get_telemetry_summary(db: Session, device_id: UUID):
    results = db.query(
        models.TelemetryMetric.metric_name,
        func.avg(func.cast(models.TelemetryData.value, Float)).label('avg'),
        func.min(func.cast(models.TelemetryData.value, Float)).label('min'),
        func.max(func.cast(models.TelemetryData.value, Float)).label('max'),
        func.max(models.TelemetryData.value).label('latest')
    ).join(models.TelemetryData).filter(
        models.TelemetryData.device_id == device_id
    ).group_by(models.TelemetryMetric.metric_name).all()
    
    return {row.metric_name: {
        "avg": round(row.avg, 2) if row.avg else None,
        "min": round(row.min, 2) if row.min else None,
        "max": round(row.max, 2) if row.max else None,
        "latest": row.latest
    } for row in results}

def get_latest_telemetry(db: Session, device_id: UUID):
    subq = db.query(
        models.TelemetryData,
        models.TelemetryMetric.metric_name,
        func.row_number().over(
            partition_by=models.TelemetryData.metric_id,
            order_by=models.TelemetryData.recorded_at.desc()
        ).label('rn')
    ).join(models.TelemetryMetric).filter(
        models.TelemetryData.device_id == device_id
    ).subquery()
    
    results = db.query(subq).filter(subq.c.rn == 1).all()
    return [{"metric_name": r.metric_name, "value": r.value, "recorded_at": r.recorded_at} for r in results]

def create_command_log(db: Session, device_id: UUID, command: schemas.CommandLogCreate):
    if command.command not in ["dispense_treat", "go_to_location"]:
        raise HTTPException(status_code=400, detail="Invalid command")
    db_command = models.CommandLog(device_id=device_id, **command.dict())
    db.add(db_command)
    db.commit()
    db.refresh(db_command)
    return db_command

def get_command_logs(db: Session, device_id: UUID, limit: int):
    return db.query(models.CommandLog).filter(
        models.CommandLog.device_id == device_id
    ).order_by(models.CommandLog.created_at.desc()).limit(limit).all()
