from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.db.models import AttendanceStatus

class AttendanceMark(BaseModel):
    student_id: UUID
    event_id: UUID

class AttendanceResponse(BaseModel):
    id: UUID
    student_id: UUID
    event_id: UUID
    status: AttendanceStatus
    checked_in_at: datetime
    
    class Config:
        from_attributes = True
