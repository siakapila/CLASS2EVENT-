from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from uuid import UUID
from app.db.database import get_db
from app.db.models import Event, Registration, Attendance, User, RoleEnum, AttendanceStatus
from app.schemas.faculty import FacultyDashboardResponse, EventAnalytics
from app.api.dependencies import get_current_user, RoleChecker

router = APIRouter(prefix="/faculty", tags=["Faculty Dashboard"])

@router.get("/dashboard/overview", response_model=FacultyDashboardResponse)
def get_dashboard_overview(
    current_user: User = Depends(RoleChecker([RoleEnum.faculty, RoleEnum.admin])),
    db: Session = Depends(get_db)
):
    total_events = db.query(Event).count()
    
    # Count unique students who ever attended an event
    total_unique_students = db.query(Attendance.student_id).distinct().count()
    
    return FacultyDashboardResponse(
        total_events=total_events,
        total_unique_students=total_unique_students
    )

@router.get("/dashboard/event/{event_id}", response_model=EventAnalytics)
def get_event_analytics(
    event_id: UUID,
    current_user: User = Depends(RoleChecker([RoleEnum.faculty, RoleEnum.admin])),
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    total_registered = db.query(Registration).filter(Registration.event_id == event_id).count()
    
    # Present count
    total_attended = db.query(Attendance).filter(
        Attendance.event_id == event_id,
        Attendance.status == AttendanceStatus.present
    ).count()
    
    # Fraud flag patterns
    fraud_flags = db.query(Attendance).filter(
        Attendance.event_id == event_id,
        Attendance.status == AttendanceStatus.fraud_flagged
    ).count()
    
    return EventAnalytics(
        event_name=event.title,
        total_registered=total_registered,
        total_attended=total_attended,
        fraud_flags=fraud_flags
    )
