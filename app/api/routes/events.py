from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.database import get_db
from app.db.models import Event, User, RoleEnum, Club
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.api.dependencies import get_current_user, RoleChecker
from app.core.aws import upload_image_to_s3

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventCreate,
    current_user: User = Depends(RoleChecker([RoleEnum.club_organizer])),
    db: Session = Depends(get_db)
):
    club = db.query(Club).filter(Club.owner_id == current_user.id).first()
    if not club:
        raise HTTPException(
            status_code=400, 
            detail="You must create a Club first before hosting events."
        )
        
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        how_to_play=event_data.how_to_play,
        is_outhouse=event_data.is_outhouse,
        walk_ins_allowed=event_data.walk_ins_allowed,
        date=event_data.date,
        location=event_data.location,
        max_capacity=event_data.max_capacity,
        club_id=club.id
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: UUID,
    event_data: EventUpdate,
    current_user: User = Depends(RoleChecker([RoleEnum.club_organizer])),
    db: Session = Depends(get_db)
):
    club = db.query(Club).filter(Club.owner_id == current_user.id).first()
    event = db.query(Event).filter(Event.id == event_id, Event.club_id == club.id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found or you don't own it")
        
    update_data = event_data.model_dump(exclude_unset=True) # Pydantic v2
    for key, value in update_data.items():
        setattr(event, key, value)
        
    db.commit()
    db.refresh(event)
    return event

@router.post("/{event_id}/upload-qr", response_model=EventResponse)
async def upload_payment_qr(
    event_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(RoleChecker([RoleEnum.club_organizer])),
    db: Session = Depends(get_db)
):
    club = db.query(Club).filter(Club.owner_id == current_user.id).first()
    event = db.query(Event).filter(Event.id == event_id, Event.club_id == club.id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    # Upload to AWS S3
    url = upload_image_to_s3(file, folder="payment_qrs")
    
    event.payment_qr_url = url
    db.commit()
    db.refresh(event)
    return event

@router.get("/", response_model=List[EventResponse])
def get_all_events(
    search: str = None,
    club_id: UUID = None,
    is_outhouse: bool = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    
    if search:
        # Use database indexes already created for fast search
        query = query.filter(
            (Event.title.ilike(f"%{search}%")) | 
            (Event.description.ilike(f"%{search}%"))
        )
    
    if club_id:
        query = query.filter(Event.club_id == club_id)
        
    if is_outhouse is not None:
        query = query.filter(Event.is_outhouse == is_outhouse)
        
    events = query.order_by(Event.date.asc()).all()
    return events
