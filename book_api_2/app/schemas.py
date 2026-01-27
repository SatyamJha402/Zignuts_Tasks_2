from sqlmodel import SQLModel
from typing import Optional

class BookBase(SQLModel):
    title: str
    author: str
    year: Optional[int] = None

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int
    owner_id: int