from pydantic import BaseModel, EmailStr
from typing import Optional, List


#schema for user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "job_seeker"

#Schema for reading user data
class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str

#schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


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
    # tags: List[str] = []
    
    class Config:
        form_attribute = True

#Update job schema
class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None