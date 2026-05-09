from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeviceCreate(BaseModel):
    device_id: str
    name: str
    device_type: str
    location: str | None = None
    

class DeviceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: str
    name: str
    device_type: str
    location: str | None
    status: str
    created_at: datetime
    updated_at: datetime