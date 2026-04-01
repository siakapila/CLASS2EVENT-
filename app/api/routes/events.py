from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Event, User, RoleEnum, Club
from app.schemas.event import EventCreate, EventResponse
from app.api.dependencies import get_current_user, RoleChecker

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventCreate,
    current_user: User = Depends(RoleChecker([RoleEnum.club_organizer])),
    db: Session = Depends(get_db)
):
    # Ensure this organizer actually has a club to host events under
    club = db.query(Club).filter(Club.owner_id == current_user.id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You must create a Club first before hosting events."
        )
        
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        date=event_data.date,
        location=event_data.location,
        max_capacity=event_data.max_capacity,
        club_id=club.id
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/", response_model=List[EventResponse])
def get_all_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events
