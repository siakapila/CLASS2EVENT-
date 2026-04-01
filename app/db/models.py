import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Enum as SQLEnum, UniqueConstraint, Boolean, UUID
from sqlalchemy.orm import relationship
from .database import Base
import enum

class RoleEnum(str, enum.Enum):
    student = "student"
    club_organizer = "club_organizer"
    faculty = "faculty"
    admin = "admin"

class AttendanceStatus(str, enum.Enum):
    present = "present"
    fraud_flagged = "fraud_flagged"

class RequestStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.student, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    faculty_profile = relationship("FacultyProfile", back_populates="user", uselist=False)
    clubs = relationship("Club", back_populates="owner")
    registrations = relationship("Registration", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    team_memberships = relationship("TeamMember", back_populates="student")
    organising_requests = relationship("EventOrganiser", back_populates="student")

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    registration_number = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=False)
    course = Column(String, nullable=False)
    year = Column(Integer, nullable=False) # 1-5
    section = Column(String, nullable=False)
    
    user = relationship("User", back_populates="student_profile")

class FacultyProfile(Base):
    __tablename__ = "faculty_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    department = Column(String, nullable=False)
    course = Column(String, nullable=False)
    
    user = relationship("User", back_populates="faculty_profile")

class Club(Base):
    __tablename__ = "clubs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="clubs")
    events = relationship("Event", back_populates="club")

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    how_to_play = Column(Text)
    is_outhouse = Column(Boolean, default=False)
    walk_ins_allowed = Column(Boolean, default=False)
    payment_qr_url = Column(String, nullable=True)
    club_id = Column(UUID(as_uuid=True), ForeignKey("clubs.id"), nullable=False)
    date = Column(DateTime, nullable=True) # Optional upon creation
    location = Column(String, nullable=True) # Optional upon creation
    max_capacity = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    club = relationship("Club", back_populates="events")
    registrations = relationship("Registration", back_populates="event")
    attendances = relationship("Attendance", back_populates="event")
    organisers = relationship("EventOrganiser", back_populates="event")

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    upi_transaction_id = Column(String, nullable=True)
    payment_screenshot_url = Column(String, nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('student_id', 'event_id', name='uq_student_event_registration'),
    )

    student = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
    team_members = relationship("TeamMember", back_populates="registration")

class TeamMember(Base):
    __tablename__ = "team_members"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_id = Column(UUID(as_uuid=True), ForeignKey("registrations.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False) # The invited teammate
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.pending)
    
    __table_args__ = (
        UniqueConstraint('registration_id', 'student_id', name='uq_team_member'),
    )
    
    registration = relationship("Registration", back_populates="team_members")
    student = relationship("User", back_populates="team_memberships")

class EventOrganiser(Base):
    __tablename__ = "event_organisers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.pending)
    
    __table_args__ = (
        UniqueConstraint('event_id', 'student_id', name='uq_event_organiser'),
    )
    
    event = relationship("Event", back_populates="organisers")
    student = relationship("User", back_populates="organising_requests")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    status = Column(SQLEnum(AttendanceStatus), default=AttendanceStatus.present, nullable=False)
    checked_in_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('student_id', 'event_id', name='uq_student_event_attendance'),
    )

    student = relationship("User", back_populates="attendances")
    event = relationship("Event", back_populates="attendances")
