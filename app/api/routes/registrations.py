from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from uuid import UUID
from app.db.database import get_db
from app.db.models import Registration, Event, User, RoleEnum
from app.schemas.registration import RegistrationResponse, RegistrationWithEvent
from app.api.dependencies import get_current_user, RoleChecker

router = APIRouter(prefix="/registrations", tags=["Registrations"])

@router.post("/{event_id}", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_for_event(
    event_id: UUID,
    current_user: User = Depends(RoleChecker([RoleEnum.student])),
    db: Session = Depends(get_db)
):
    # Verify the event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    # Check max capacity if defined
    if event.max_capacity:
        current_registrations = db.query(Registration).filter(Registration.event_id == event_id).count()
        if current_registrations >= event.max_capacity:
            raise HTTPException(status_code=400, detail="Event is already at full capacity")
            
    # Create registration
    try:
        new_reg = Registration(
            student_id=current_user.id,
            event_id=event_id
        )
        db.add(new_reg)
        db.commit()
        db.refresh(new_reg)
        return new_reg
    except IntegrityError:
        db.rollback()
        # This catches our unique constraint uq_student_event_registration
        raise HTTPException(status_code=400, detail="You are already registered for this event")

@router.get("/my-registrations", response_model=List[RegistrationWithEvent])
def get_my_registrations(
    current_user: User = Depends(get_current_user), # Any logged-in user can check their own
    db: Session = Depends(get_db)
):
    registrations = db.query(Registration).filter(Registration.student_id == current_user.id).all()
    return registrations
