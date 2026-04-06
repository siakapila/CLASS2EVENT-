from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base
from app.api.routes import auth, clubs, events, registrations, attendance, faculty, analytics, reports

# Tell SQLAlchemy to automatically create out tables in Postgres
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(clubs.router)
app.include_router(events.router)
app.include_router(registrations.router)
app.include_router(attendance.router)
app.include_router(faculty.router)
app.include_router(analytics.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
