from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.schemas import UserCreate, UserRead, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import require_recruiter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends


router = APIRouter(prefix="/auth", tags=["auth"])

#User registration endpoint
@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    #Check if user with the same email already exists
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    #Create new user
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

#User login endpoint
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    db_user = session.exec(
        select(User).where(User.email == form_data.username)
    ).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({
        "sub": db_user.email,
        "role": db_user.role
    })
    return {"access_token": token, "token_type": "bearer"}



#Protected endpoint for recruiters only
@router.get("/recruiter-only")
def recruiter_only_test(current_user=Depends(require_recruiter)):
    return {"message": f"Hello recruiter {current_user.email}!"}