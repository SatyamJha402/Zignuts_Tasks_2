from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Book
from app.auth import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

#List all books
@router.get("/", response_model=List[Book])
def list_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()

#Get a specific book by ID
@router.post("/", response_model=Book)
def create_book(
    book: Book,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)   # 🔒 protected
):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

#Get a specific book by ID
@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    updated: Book,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)   # 🔒 protected
):
    book = session.get(Book, book_id)
    # Check if the book exists
    if not book:
        raise HTTPException(status_code=404)

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
    user=Depends(get_current_user)   # 🔒 protected
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404)

    session.delete(book)
    session.commit()
    return {"message": "Book deleted"}