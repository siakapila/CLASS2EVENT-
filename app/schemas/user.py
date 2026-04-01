from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID
from datetime import datetime
from app.db.models import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class StudentSignup(UserBase):
    password: str
    registration_number: str
    department: str
    course: str
    year: int = Field(ge=1, le=5)
    section: str

    @field_validator('email')
    @classmethod
    def validate_domain(cls, v):
        if not v.endswith('@muj.manipal.edu'):
            raise ValueError('Students must strictly use @muj.manipal.edu email domain')
        return v

class FacultySignup(UserBase):
    password: str
    department: str
    course: str

    @field_validator('email')
    @classmethod
    def validate_domain(cls, v):
        if not v.endswith('@jaipur.manipal.edu'):
            raise ValueError('Faculty must strictly use @jaipur.manipal.edu email domain')
        return v

class ClubSignup(UserBase):
    password: str

    @field_validator('email')
    @classmethod
    def validate_domain(cls, v):
        if not v.endswith('@muj.manipal.edu'):
            raise ValueError('Clubs must strictly use @muj.manipal.edu email domain')
        return v

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class UserResponse(UserBase):
    id: UUID
    role: RoleEnum
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
