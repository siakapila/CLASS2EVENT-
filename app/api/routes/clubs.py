from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Club, User, RoleEnum
from app.schemas.club import ClubCreate, ClubResponse
from app.api.dependencies import get_current_user, RoleChecker

router = APIRouter(prefix="/clubs", tags=["Clubs"])

@router.post("/", response_model=ClubResponse, status_code=status.HTTP_201_CREATED)
def create_club(
    club_data: ClubCreate,
    current_user: User = Depends(RoleChecker([RoleEnum.club_organizer])),
    db: Session = Depends(get_db)
):
    existing = db.query(Club).filter(Club.name == club_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Club name already exists")
        
    new_club = Club(
        name=club_data.name,
        description=club_data.description,
        owner_id=current_user.id
    )
    db.add(new_club)
    db.commit()
    db.refresh(new_club)
    return new_club

@router.get("/", response_model=List[ClubResponse])
def list_clubs(db: Session = Depends(get_db)):
    return db.query(Club).all()
