from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_session
from app.models import User
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

#User registration
@router.post("/register")
def register(username: str, password: str, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.username == username)).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    return {"message": "User registered successfully"}

#User login
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    #Find the user by username
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    #Verify password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    #Create JWT token
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}