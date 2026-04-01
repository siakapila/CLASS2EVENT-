from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.schemas.event import EventResponse

class RegistrationBase(BaseModel):
    pass

class RegistrationCreate(RegistrationBase):
    event_id: UUID

class RegistrationResponse(RegistrationBase):
    id: UUID
    student_id: UUID
    event_id: UUID
    registered_at: datetime
    
    class Config:
        from_attributes = True

class RegistrationWithEvent(RegistrationResponse):
    event: EventResponse
