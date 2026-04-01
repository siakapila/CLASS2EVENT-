from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth, clubs, events

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(auth.router)
app.include_router(clubs.router)
app.include_router(events.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
