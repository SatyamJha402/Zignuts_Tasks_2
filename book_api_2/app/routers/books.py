from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Book
from app.auth import get_current_user
from app.schemas import BookCreate, BookRead

router = APIRouter(tags=["Books"])

#List all books
@router.get("/", response_model=List[Book])
def list_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()

#Create a new book
@router.post("/", response_model=BookRead)
def create_book(
    book: BookCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    db_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        owner_id=user.id
    )

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

#Update an existing book
@router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    updated: BookCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404)

    if book.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    book.title = updated.title
    book.author = updated.author
    book.year = updated.year

    session.commit()
    session.refresh(book)
    return book


#Delete a book by ID
@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404)

    if book.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.delete(book)
    session.commit()
    return {"message": "Book deleted"}