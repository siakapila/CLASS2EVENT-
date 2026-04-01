from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.schemas.event import EventResponse

class RegistrationBase(BaseModel):
    upi_transaction_id: Optional[str] = None

class RegistrationCreate(RegistrationBase):
    event_id: UUID
    teammate_emails: Optional[List[str]] = []

class TeamMemberResponse(BaseModel):
    id: UUID
    student_id: UUID
    status: str
    
    class Config:
        from_attributes = True

class RegistrationResponse(RegistrationBase):
    id: UUID
    student_id: UUID
    event_id: UUID
    payment_screenshot_url: Optional[str] = None
    registered_at: datetime
    team_members: List[TeamMemberResponse] = []
    
    class Config:
        from_attributes = True

class RegistrationWithEvent(RegistrationResponse):
    event: EventResponse

class OrganiserRequest(BaseModel):
    event_id: UUID

class OrganiserResponse(BaseModel):
    id: UUID
    event_id: UUID
    student_id: UUID
    status: str
    
    class Config:
        from_attributes = True
