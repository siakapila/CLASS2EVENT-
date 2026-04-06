import uuid
from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, User, RoleEnum, Club, Event, Registration, Attendance, AttendanceStatus
from app.core.security import get_password_hash

DATABASE_URL = "sqlite:///./campus_events.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    db = SessionLocal()
    
    # 1. Create a Club Organizer
    organizer_email = "organizer@university.edu"
    existing_org = db.query(User).filter(User.email == organizer_email).first()
    if not existing_org:
        organizer = User(
            email=organizer_email,
            hashed_password=get_password_hash("password123"),
            full_name="Alex Johnson",
            role=RoleEnum.club_organizer,
            is_verified=True
        )
        db.add(organizer)
        db.commit()
        db.refresh(organizer)
    else:
        organizer = existing_org

    # 2. Create a Club
    club_name = "Tech Innovators Club"
    existing_club = db.query(Club).filter(Club.name == club_name).first()
    if not existing_club:
        club = Club(
            name=club_name,
            description="Leading the campus in tech events and hackathons.",
            owner_id=organizer.id
        )
        db.add(club)
        db.commit()
        db.refresh(club)
    else:
        club = existing_club

    # 3. Create Sample Events
    event_titles = [
        "Global Hackathon 2024", "AI Workshop: Future of Coding", "CyberSecurity Summit", 
        "Cloud Native Meetup", "Web3 Revolution Seminar", "UI/UX Design Sprint", 
        "Open Source Fest", "Machine Learning Bootcamp", "Robotics Challenge", 
        "Data Science Symposium", "DevOps Day", "Mobile App Dev Workshop",
        "Blockchain Basics", "Quantum Computing Intro", "AR/VR Experience"
    ]
    
    events = []
    for title in event_titles:
        existing_event = db.query(Event).filter(Event.title == title).first()
        if not existing_event:
            event = Event(
                title=title,
                description=f"Deep dive into {title} with industry experts.",
                club_id=club.id,
                date=datetime.utcnow() + timedelta(days=random.randint(1, 60)),
                location="Main Auditorium",
                max_capacity=500
            )
            db.add(event)
            events.append(event)
        else:
            events.append(existing_event)
    
    db.commit()

    # 4. Create Students and Registrations/Attendance
    # We want impressive metrics: High registration numbers, varying attendance rates
    student_count = 500
    students = []
    for i in range(student_count):
        email = f"student{i}@university.edu"
        existing_student = db.query(User).filter(User.email == email).first()
        if not existing_student:
            student = User(
                email=email,
                hashed_password=get_password_hash("password123"),
                full_name=f"Student {i}",
                role=RoleEnum.student,
                is_verified=True
            )
            db.add(student)
            students.append(student)
        else:
            students.append(existing_student)
    
    db.commit()

    for event in events:
        # Each event gets a random number of registrations (100-300)
        reg_count = random.randint(100, 300)
        selected_students = random.sample(students, reg_count)
        
        for student in selected_students:
            existing_reg = db.query(Registration).filter(
                Registration.student_id == student.id, 
                Registration.event_id == event.id
            ).first()
            
            if not existing_reg:
                reg = Registration(
                    student_id=student.id,
                    event_id=event.id,
                    registered_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
                )
                db.add(reg)
                
                # Simulate Attendance (70-95% attendance rate for "impressive" metrics)
                if random.random() < 0.88:
                    existing_att = db.query(Attendance).filter(
                        Attendance.student_id == student.id,
                        Attendance.event_id == event.id
                    ).first()
                    
                    if not existing_att:
                        att = Attendance(
                            student_id=student.id,
                            event_id=event.id,
                            status=AttendanceStatus.present,
                            checked_in_at=event.date + timedelta(minutes=random.randint(-15, 45)) if event.date else datetime.utcnow()
                        )
                        db.add(att)

    db.commit()
    print("Successfully seeded metrics data!")

if __name__ == "__main__":
    seed_data()
