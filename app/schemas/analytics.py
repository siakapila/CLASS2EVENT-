from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID

class EventStats(BaseModel):
    event_id: UUID
    title: str
    registrations: int
    attendance: int
    attendance_rate: float

class DashboardStats(BaseModel):
    total_events: int
    total_registrations: int
    total_attendance: int
    avg_attendance_rate: float
    event_performance: List[EventStats]
    registration_trends: List[Dict[str, int]] # Date and count
