from datetime import timedelta
import random
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, StudentProfile, FacultyProfile, Club, RoleEnum
from app.schemas.user import StudentSignup, FacultySignup, ClubSignup, VerifyOTP, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.core.email import send_verification_email

router = APIRouter(prefix="/auth", tags=["Authentication & Verification"])

# In-memory OTP store (Use Redis for production)
otp_store = {}

async def process_user_creation(email, password, full_name, role, db):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_pass = get_password_hash(password)
    new_user = User(
        email=email,
        full_name=full_name,
        role=role,
        hashed_password=hashed_pass,
        is_verified=False # Must verify OTP to login
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate and send OTP
    otp_code = str(random.randint(100000, 999999))
    otp_store[email] = otp_code
    await send_verification_email(email, otp_code)
    
    return new_user

@router.post("/signup/student", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup_student(user: StudentSignup, db: Session = Depends(get_db)):
    new_user = await process_user_creation(user.email, user.password, user.full_name, RoleEnum.student, db)
    
    # Store extended fields
    profile = StudentProfile(
        user_id=new_user.id,
        registration_number=user.registration_number,
        department=user.department,
        course=user.course,
        year=user.year,
        section=user.section
    )
    db.add(profile)
    db.commit()
    return new_user

@router.post("/signup/faculty", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup_faculty(user: FacultySignup, db: Session = Depends(get_db)):
    new_user = await process_user_creation(user.email, user.password, user.full_name, RoleEnum.faculty, db)
    profile = FacultyProfile(
        user_id=new_user.id,
        department=user.department,
        course=user.course
    )
    db.add(profile)
    db.commit()
    return new_user

@router.post("/signup/club", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup_club(user: ClubSignup, db: Session = Depends(get_db)):
    new_user = await process_user_creation(user.email, user.password, user.full_name, RoleEnum.club_organizer, db)
    # Give them a club entity automatically
    club = Club(
        name=user.full_name,
        owner_id=new_user.id
    )
    db.add(club)
    db.commit()
    return new_user

@router.post("/verify-otp")
def verify_email_otp(data: VerifyOTP, db: Session = Depends(get_db)):
    if data.email not in otp_store or otp_store[data.email] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.is_verified = True
    db.commit()
    
    del otp_store[data.email]
    return {"message": "Email verified successfully! You can now login."}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Check your email and verify your OTP before logging in.")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
