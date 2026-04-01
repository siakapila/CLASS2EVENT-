from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.db.database import get_db
from app.db.models import Event, Registration, Attendance, User, RoleEnum, AttendanceStatus, StudentProfile, EventOrganiser, RequestStatus
from app.schemas.faculty import FacultyDashboardResponse, FacultyEventDashboard, StudentDetail
from app.api.dependencies import RoleChecker

router = APIRouter(prefix="/faculty", tags=["Faculty Dashboard"])

@router.get("/dashboard/overview", response_model=FacultyDashboardResponse)
def get_dashboard_overview(
    current_user: User = Depends(RoleChecker([RoleEnum.faculty, RoleEnum.admin])),
    db: Session = Depends(get_db)
):
    total_events = db.query(Event).count()
    total_unique_students = db.query(Attendance.student_id).distinct().count()
    
    return FacultyDashboardResponse(
        total_events=total_events,
        total_unique_students=total_unique_students
    )

@router.get("/dashboard/event/{event_id}", response_model=FacultyEventDashboard)
def get_event_analytics(
    event_id: UUID,
    current_user: User = Depends(RoleChecker([RoleEnum.faculty, RoleEnum.admin])),
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    total_registered = db.query(Registration).filter(Registration.event_id == event_id).count()
    
    # Base attendance metrics
    base_attendance = db.query(Attendance).filter(Attendance.event_id == event_id)
    total_attended = base_attendance.filter(Attendance.status == AttendanceStatus.present).count()
    fraud_flags = base_attendance.filter(Attendance.status == AttendanceStatus.fraud_flagged).count()
    
    # 1. Get Organisers (Yellow Dot equivalent)
    # We must join User and StudentProfile, and filter for accepted organiser requests
    approved_organisers = db.query(User, StudentProfile).join(
        StudentProfile, User.id == StudentProfile.user_id
    ).join(
        EventOrganiser, User.id == EventOrganiser.student_id
    ).filter(
        EventOrganiser.event_id == event_id,
        EventOrganiser.status == RequestStatus.accepted
    ).order_by(
        StudentProfile.department,
        StudentProfile.course,
        StudentProfile.section,
        User.full_name
    ).all()
    
    organiser_ids = []
    organiser_list = []
    for user, profile in approved_organisers:
        organiser_ids.append(user.id)
        organiser_list.append(StudentDetail(
            id=user.id,
            full_name=user.full_name,
            registration_number=profile.registration_number,
            department=profile.department,
            course=profile.course,
            year=profile.year,
            section=profile.section
        ))
        
    # 2. Get Standard Participants (Green Dot equivalent)
    # They should be present in Attendance, and NOT be one of the existing organisers
    participants_query = db.query(User, StudentProfile).join(
        StudentProfile, User.id == StudentProfile.user_id
    ).join(
        Attendance, User.id == Attendance.student_id
    ).filter(
        Attendance.event_id == event_id,
        Attendance.status == AttendanceStatus.present
    )
    
    if organiser_ids:
        participants_query = participants_query.filter(User.id.notin_(organiser_ids))
        
    # The magical sorting logic by Dept -> Course -> Section -> Name
    participants_query = participants_query.order_by(
        StudentProfile.department,
        StudentProfile.course,
        StudentProfile.section,
        User.full_name
    ).all()
    
    participant_list = []
    for user, profile in participants_query:
        participant_list.append(StudentDetail(
            id=user.id,
            full_name=user.full_name,
            registration_number=profile.registration_number,
            department=profile.department,
            course=profile.course,
            year=profile.year,
            section=profile.section
        ))
        
    return FacultyEventDashboard(
        event_name=event.title,
        total_registered=total_registered,
        total_attended=total_attended,
        fraud_flags=fraud_flags,
        organisers=organiser_list,
        participants=participant_list
    )
