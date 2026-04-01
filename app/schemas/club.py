from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class ClubBase(BaseModel):
    name: str
    description: Optional[str] = None

class ClubCreate(ClubBase):
    pass

class ClubResponse(ClubBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
