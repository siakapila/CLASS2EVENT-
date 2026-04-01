# Campus Event & Attendance Management System

A production-ready backend built with FastAPI and PostgreSQL for managing university clubs, events, student registrations, and check-in attendance. 

## Features
- **Role-Based Access Control**: Student, Club Organizer, Faculty, and Admin.
- **Event Creation**: Authorized clubs can plan and schedule campus events.
- **Registration**: Students can register to enter events safely.
- **Attendance Verification**: Prevent duplicate check-ins and fraud (e.g., proxy entries).
- **Security**: JWT-based session auth and bcrypt password hashing.

## Tech Stack
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy + Alembic (Migrations)
- **Auth**: Passlib + Python-JOSE

## Running the Application Locally
1. Clone the repository.
2. Set up a virtual environment: `python -m venv venv`
3. Activate the virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Configure your database details inside `.env`
6. Run the local dev server using: `uvicorn app.main:app --reload`
