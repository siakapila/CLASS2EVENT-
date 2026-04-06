import io
import csv
from fastapi import APIRouter, Depends, HTTPException, status, Response, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.db.models import Event, Registration, User, RoleEnum, Club
from app.api.dependencies import get_current_user, RoleChecker

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/events/{event_id}/registrations/csv")
def export_registrations_csv(
    event_id: UUID,
    current_user: User = Depends(RoleChecker([RoleEnum.club_organizer, RoleEnum.faculty, RoleEnum.admin])),
    db: Session = Depends(get_db)
):
    # Check ownership
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    # Permission Check
    if current_user.role == RoleEnum.club_organizer:
        club = db.query(Club).filter(Club.owner_id == current_user.id).first()
        if not club or club.id != event.club_id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not own this event")

    registrations = db.query(Registration).filter(Registration.event_id == event_id).all()
    
    # Create CSV in-memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student ID", "Full Name", "Email", "Registered At", "Transaction ID"])
    
    for reg in registrations:
        writer.writerow([
            reg.student.id,
            reg.student.full_name,
            reg.student.email,
            reg.student.registered_at,
            reg.upi_transaction_id or "N/A"
        ])
    
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=registrations_{event_id}.csv"
    return response

@router.get("/summary/csv")
def export_club_summary_csv(
    current_user: User = Depends(RoleChecker([RoleEnum.club_organizer, RoleEnum.faculty, RoleEnum.admin])),
    db: Session = Depends(get_db)
):
    # For a club organizer, export all their events' summary
    club = db.query(Club).filter(Club.owner_id == current_user.id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
        
    events = db.query(Event).filter(Event.club_id == club.id).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Event Title", "Date", "Registrations", "Attendance", "Attendance Rate %"])
    
    for event in events:
        reg_count = db.query(Registration).filter(Registration.event_id == event.id).count()
        att_count = db.query(Registration).filter(Registration.event_id == event.id).count() # Simplified for this demo
        rate = (att_count / reg_count * 100) if reg_count > 0 else 0
        
        writer.writerow([
            event.title,
            event.date,
            reg_count,
            att_count,
            round(rate, 2)
        ])
        
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=club_summary.csv"
    return response
