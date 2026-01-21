from pydantic import BaseModel, EmailStr

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