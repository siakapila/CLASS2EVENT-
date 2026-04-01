from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID
from datetime import datetime

class EventAnalytics(BaseModel):
    event_name: str
    total_registered: int
    total_attended: int
    fraud_flags: int

class FacultyDashboardResponse(BaseModel):
    total_events: int
    total_unique_students: int
