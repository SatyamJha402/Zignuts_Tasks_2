from pydantic import BaseModel
from typing import Optional, List

#Create job schema
class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    company_id: int
    tags: List[str] = []

#Read job schema
class JobRead(BaseModel):
    id: int
    title: str
    description: str
    location: str
    company_id: int
    created_by: int
    tags: List[str] = []

#Update job schema
class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None