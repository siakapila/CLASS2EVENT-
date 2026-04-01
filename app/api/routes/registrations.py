from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from uuid import UUID
from app.db.database import get_db
from app.db.models import Registration, Event, User, RoleEnum, TeamMember, RequestStatus, EventOrganiser, Club
from app.schemas.registration import RegistrationResponse, RegistrationCreate, RegistrationWithEvent, OrganiserRequest, OrganiserResponse
from app.api.dependencies import get_current_user, RoleChecker
from app.core.aws import upload_image_to_s3

router = APIRouter(prefix="/registrations", tags=["Registrations & Organisers"])

@router.post("/", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_for_event(
    data: RegistrationCreate,
    current_user: User = Depends(RoleChecker([RoleEnum.student])),
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    teammates_count = len(data.teammate_emails) if data.teammate_emails else 0
    if event.max_capacity:
        current_registrations = db.query(Registration).filter(Registration.event_id == data.event_id).count()
        if current_registrations + teammates_count + 1 > event.max_capacity:
            raise HTTPException(status_code=400, detail="Not enough capacity remaining for this team size")

    try:
        new_reg = Registration(
            student_id=current_user.id,
            event_id=data.event_id,
            upi_transaction_id=data.upi_transaction_id
        )
        db.add(new_reg)
        db.flush() # Flush to get new_reg.id without committing fully
        
        # Add teammates
        if data.teammate_emails:
            for email in data.teammate_emails:
                teammate = db.query(User).filter(User.email == email, User.role == RoleEnum.student).first()
                if not teammate:
                    db.rollback()
                    raise HTTPException(status_code=400, detail=f"Student account not found for teammate: {email}")
                
                member = TeamMember(
                    registration_id=new_reg.id,
                    student_id=teammate.id,
                    status=RequestStatus.pending
                )
                db.add(member)
            
        db.commit()
        db.refresh(new_reg)
        return new_reg
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="You are already registered.")

@router.post("/{registration_id}/upload-payment-screenshot", response_model=RegistrationResponse)
async def upload_payment_screenshot(
    registration_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(RoleChecker([RoleEnum.student])),
    db: Session = Depends(get_db)
):
    reg = db.query(Registration).filter(Registration.id == registration_id, Registration.student_id == current_user.id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")
        
    url = upload_image_to_s3(file, folder="payment_screenshots")
    reg.payment_screenshot_url = url
    db.commit()
    db.refresh(reg)
    return reg

@router.post("/teammates/accept/{team_member_id}")
def accept_team_invitation(
    team_member_id: UUID,
    current_user: User = Depends(RoleChecker([RoleEnum.student])),
    db: Session = Depends(get_db)
):
    tm = db.query(TeamMember).filter(TeamMember.id == team_member_id, TeamMember.student_id == current_user.id).first()
    if not tm:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    tm.status = RequestStatus.accepted
    db.commit()
    return {"message": "You have officially accepted the invitation and joined the team."}

@router.post("/organisers/request", response_model=OrganiserResponse)
def request_to_organize(
    data: OrganiserRequest,
    current_user: User = Depends(RoleChecker([RoleEnum.student])),
    db: Session = Depends(get_db)
):
    try:
        new_req = EventOrganiser(
            student_id=current_user.id,
            event_id=data.event_id,
            status=RequestStatus.pending
        )
        db.add(new_req)
        db.commit()
        db.refresh(new_req)
        return new_req
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="You have already submitted a request for this event.")

@router.post("/organisers/approve/{request_id}")
def approve_organiser(
    request_id: UUID,
    current_user: User = Depends(RoleChecker([RoleEnum.club_organizer])),
    db: Session = Depends(get_db)
):
    req = db.query(EventOrganiser).filter(EventOrganiser.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Organiser request not found")
        
    # Security: check if the club owner is the one approving
    event = db.query(Event).filter(Event.id == req.event_id, Event.club_id.in_(
        db.query(Club.id).filter(Club.owner_id == current_user.id)
    )).first()
    
    if not event:
        raise HTTPException(status_code=403, detail="You do not own this event!")
        
    req.status = RequestStatus.accepted
    db.commit()
    return {"message": "Organiser approved successfully."}

@router.get("/my-registrations", response_model=List[RegistrationWithEvent])
def get_my_registrations(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    registrations = db.query(Registration).filter(Registration.student_id == current_user.id).all()
    return registrations
