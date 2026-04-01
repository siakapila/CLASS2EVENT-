from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    how_to_play: Optional[str] = None
    is_outhouse: bool = False
    walk_ins_allowed: bool = False
    date: Optional[datetime] = None
    location: Optional[str] = None
    max_capacity: Optional[int] = None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    how_to_play: Optional[str] = None
    is_outhouse: Optional[bool] = None
    walk_ins_allowed: Optional[bool] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    max_capacity: Optional[int] = None

class EventResponse(EventBase):
    id: UUID
    club_id: UUID
    payment_qr_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
