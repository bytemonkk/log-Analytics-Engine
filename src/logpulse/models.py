from datetime import datetime

from pydantic import BaseModel, Field


class LogEvent(BaseModel):
    timestamp: datetime
    request_id: str
    service: str
    method: str
    endpoint: str
    status_code: int = Field(ge=100, le=599)
    latency_ms: float = Field(ge=0)
    response_bytes: int = Field(ge=0)
    client_ip: str