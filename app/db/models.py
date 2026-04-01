import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
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
    absent = "absent"
    fraud_flagged = "fraud_flagged"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.student, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    clubs = relationship("Club", back_populates="owner")
    registrations = relationship("Registration", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")

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
    club_id = Column(UUID(as_uuid=True), ForeignKey("clubs.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    max_capacity = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    club = relationship("Club", back_populates="events")
    registrations = relationship("Registration", back_populates="event")
    attendances = relationship("Attendance", back_populates="event")

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('student_id', 'event_id', name='uq_student_event_registration'),
    )

    student = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")

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
