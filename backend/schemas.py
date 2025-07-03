from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import datetime
from typing import Optional

class RobotDeviceBase(BaseModel):
    device_name: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)

class RobotDeviceCreate(RobotDeviceBase):
    pass

class RobotDevice(RobotDeviceBase):
    device_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class TelemetryMetricBase(BaseModel):
    metric_name: str = Field(..., min_length=1)
    metric_unit: str = Field(..., min_length=1)

class TelemetryMetricCreate(TelemetryMetricBase):
    pass

class TelemetryMetric(TelemetryMetricBase):
    metric_id: UUID

    class Config:
        orm_mode = True

class TelemetryDataBase(BaseModel):
    metric_name: str
    value: str

class TelemetryDataCreate(TelemetryDataBase):
    @validator('value')
    def validate_value(cls, v, values):
        metric_name = values.get('metric_name')
        try:
            if metric_name == 'battery_level':
                val = float(v)
                if not 0 <= val <= 100:
                    raise ValueError('Battery must be between 0 and 100%')
            elif metric_name == 'temperature':
                val = float(v)
                if not 0 <= val <= 80:
                    raise ValueError('Temperature must be between 0 and 80°C')
            elif metric_name == 'feed_dispensed':
                val = float(v)
                if not 0 <= val <= 2000:
                    raise ValueError('Feed dispensed must be between 0 and 2000 grams')
            elif metric_name in ['play_sessions', 'feeding_times', 'task_count', 'health_alerts', 'camera_usage', 'training_sessions']:
                val = int(v)
                if val < 0:
                    raise ValueError(f'{metric_name} cannot be negative')
            elif metric_name == 'activity_duration':
                val = float(v)
                if val < 0:
                    raise ValueError('Activity duration cannot be negative')
            return v
        except ValueError as e:
            raise ValueError(f'Invalid value for {metric_name}: {str(e)}')

class TelemetryData(TelemetryDataBase):
    data_id: UUID
    device_id: UUID
    metric_id: UUID
    recorded_at: datetime

    class Config:
        orm_mode = True

class CommandLogBase(BaseModel):
    command: str = Field(..., min_length=1)

class CommandLogCreate(CommandLogBase):
    pass

class CommandLog(CommandLogBase):
    command_id: UUID
    device_id: UUID
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
