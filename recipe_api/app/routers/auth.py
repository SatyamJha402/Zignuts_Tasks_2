from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_session
from app.models import User, UserCreate, UserRead
from app.auth import hash_password, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

#Registration endpoint
@router.post("/register", response_model=UserRead)
def register(
    user: UserCreate,
    session: Session = Depends(get_session),
):
    # Check if user already exists
    statement = select(User).where(User.username == user.username)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    # Create new user
    db_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    # Save user to the database
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


#Login endpoint
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    # Create JWT token
    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }