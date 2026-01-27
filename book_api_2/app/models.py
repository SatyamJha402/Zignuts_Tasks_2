from sqlmodel import SQLModel, Field
from typing import Optional

# User table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str


# Book table
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    year: Optional[int] = None

    owner_id: int = Field(foreign_key="user.id", index=True)