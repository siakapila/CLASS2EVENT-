from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    location: str
    max_capacity: Optional[int] = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: UUID
    club_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
