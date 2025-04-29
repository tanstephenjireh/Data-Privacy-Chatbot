from pydantic import BaseModel
from datetime import datetime

class TelemetryBase(BaseModel):
    endpoint: str
    input: str
    start_time: datetime | None
    end_time: datetime | None
    status: str
    response: str

class TelemetryRead(TelemetryBase):
    id: int