from fastapi import FastAPI
from app.core.config import settings
from app.db.database import engine, Base
from app.api.routes import auth, clubs, events, registrations, attendance, faculty

# Tell SQLAlchemy to automatically create out tables in Postgres
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(auth.router)
app.include_router(clubs.router)
app.include_router(events.router)
app.include_router(registrations.router)
app.include_router(attendance.router)
app.include_router(faculty.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
