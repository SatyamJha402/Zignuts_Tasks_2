from pydantic import BaseModel
from typing import Optional

#Pydantic schemas for Company
class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CompanyRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None