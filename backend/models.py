from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

class RobotDevice(Base):
    __tablename__ = "robot_devices"
    device_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    device_name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TelemetryMetric(Base):
    __tablename__ = "telemetry_metrics"
    metric_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    metric_name = Column(String, nullable=False, unique=True)
    metric_unit = Column(String, nullable=False)

class TelemetryData(Base):
    __tablename__ = "telemetry_data"
    data_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    device_id = Column(PG_UUID(as_uuid=True), ForeignKey("robot_devices.device_id"))
    metric_id = Column(PG_UUID(as_uuid=True), ForeignKey("telemetry_metrics.metric_id"))
    value = Column(String, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class CommandLog(Base):
    __tablename__ = "command_logs"
    command_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    device_id = Column(PG_UUID(as_uuid=True), ForeignKey("robot_devices.device_id"))
    command = Column(String, nullable=False)
    status = Column(String, default="sent")
    created_at = Column(DateTime, default=datetime.utcnow)
