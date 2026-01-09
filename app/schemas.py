from pydantic import BaseModel, ConfigDict
from datetime import datetime

class NotificationCreate(BaseModel):
    event_type: str
    payload: str

class NotificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_type: str
    payload: str
    created_at: datetime
