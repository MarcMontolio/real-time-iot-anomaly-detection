from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TelemetryEventCreate(BaseModel):
    device_id: int
    metric_name: str
    metric_value: float
    timestamp: datetime
    
    
class TelemetryEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    device_id: int
    metric_name: str
    metric_value: float
    timestamp: datetime
    is_anomaly: bool = False
    anomaly_score: float | None
    created_at: datetime
    