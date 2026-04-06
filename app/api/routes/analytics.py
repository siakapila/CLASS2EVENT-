from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from app.db.database import get_db
from app.db.models import Event, Registration, Attendance, User, RoleEnum, Club
from app.schemas.analytics import DashboardStats, EventStats
from app.api.dependencies import get_current_user, RoleChecker
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_analytics(
    current_user: User = Depends(RoleChecker([RoleEnum.club_organizer, RoleEnum.faculty, RoleEnum.admin])),
    db: Session = Depends(get_db)
):
    # If club organizer, only show their club's data
    club_id = None
    if current_user.role == RoleEnum.club_organizer:
        club = db.query(Club).filter(Club.owner_id == current_user.id).first()
        if not club:
            return DashboardStats(
                total_events=0,
                total_registrations=0,
                total_attendance=0,
                avg_attendance_rate=0.0,
                event_performance=[],
                registration_trends=[]
            )
        club_id = club.id

    # 1. Base Event Query
    event_query = db.query(Event)
    if club_id:
        event_query = event_query.filter(Event.club_id == club_id)
    
    events = event_query.all()
    event_ids = [e.id for e in events]

    if not event_ids:
        return DashboardStats(
            total_events=0,
            total_registrations=0,
            total_attendance=0,
            avg_attendance_rate=0.0,
            event_performance=[],
            registration_trends=[]
        )

    # 2. Registrations Aggregate
    total_registrations = db.query(Registration).filter(Registration.event_id.in_(event_ids)).count()
    
    # 3. Attendance Aggregate
    total_attendance = db.query(Attendance).filter(Attendance.event_id.in_(event_ids)).count()
    
    # 4. Registration Trends (Last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    trends_raw = db.query(
        func.date(Registration.registered_at).label('date'),
        func.count(Registration.id).label('count')
    ).filter(
        Registration.event_id.in_(event_ids),
        Registration.registered_at >= seven_days_ago
    ).group_by(func.date(Registration.registered_at)).all()
    
    registration_trends = [{"date": str(t.date), "count": t.count} for t in trends_raw]

    # 5. Event Performance (Breakdown)
    event_performance = []
    for event in events:
        reg_count = db.query(Registration).filter(Registration.event_id == event.id).count()
        att_count = db.query(Attendance).filter(Attendance.event_id == event.id).count()
        rate = (att_count / reg_count * 100) if reg_count > 0 else 0
        
        event_performance.append(EventStats(
            event_id=event.id,
            title=event.title,
            registrations=reg_count,
            attendance=att_count,
            attendance_rate=round(rate, 2)
        ))

    avg_rate = (total_attendance / total_registrations * 100) if total_registrations > 0 else 0

    return DashboardStats(
        total_events=len(events),
        total_registrations=total_registrations,
        total_attendance=total_attendance,
        avg_attendance_rate=round(avg_rate, 2),
        event_performance=event_performance,
        registration_trends=registration_trends
    )
