from pydantic import BaseModel
from typing import List
from uuid import UUID

class StudentDetail(BaseModel):
    id: UUID
    full_name: str
    registration_number: str
    department: str
    course: str
    year: int
    section: str

    class Config:
        from_attributes = True

class FacultyDashboardResponse(BaseModel):
    total_events: int
    total_unique_students: int

class FacultyEventDashboard(BaseModel):
    event_name: str
    total_registered: int
    total_attended: int
    fraud_flags: int
    organisers: List[StudentDetail]    # Translates to Yellow Dots
    participants: List[StudentDetail]  # Translates to Green Dots
    
    class Config:
        from_attributes = True
