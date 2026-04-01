from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from uuid import UUID
from app.db.database import get_db
from app.db.models import Attendance, Registration, Event, User, RoleEnum, AttendanceStatus
from app.schemas.attendance import AttendanceResponse, AttendanceMark
from app.api.dependencies import get_current_user, RoleChecker

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/mark", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_attendance(
    data: AttendanceMark,
    current_user: User = Depends(RoleChecker([RoleEnum.faculty, RoleEnum.club_organizer])),
    db: Session = Depends(get_db)
):
    # Check if the student actually registered for the event
    registration = db.query(Registration).filter(
        Registration.student_id == data.student_id,
        Registration.event_id == data.event_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Student is not registered for this event. No proxy entries allowed."
        )
        
    # Check if they already checked in
    existing_attendance = db.query(Attendance).filter(
        Attendance.student_id == data.student_id,
        Attendance.event_id == data.event_id
    ).first()
    
    if existing_attendance:
        # Scanning again -> potential proxy scheme or duplicate scan
        # We update the status to fraud_flagged
        existing_attendance.status = AttendanceStatus.fraud_flagged
        db.commit()
        db.refresh(existing_attendance)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Duplicate Check-In! Attendance flagged for fraud. Original scan at {existing_attendance.checked_in_at}"
        )
        
    try:
        new_attendance = Attendance(
            student_id=data.student_id,
            event_id=data.event_id,
            status=AttendanceStatus.present
        )
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        return new_attendance
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database constraint error")

@router.get("/event/{event_id}", response_model=List[AttendanceResponse])
def get_event_attendance(
    event_id: UUID,
    current_user: User = Depends(RoleChecker([RoleEnum.faculty, RoleEnum.club_organizer])),
    db: Session = Depends(get_db)
):
    attendances = db.query(Attendance).filter(Attendance.event_id == event_id).all()
    return attendances
