from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional

from app.database import get_session
from app.models import Book

router = APIRouter(prefix="/books", tags=["Books"])

#Create a new book
@router.post("/", response_model=Book)
def create_book(book: Book, session: Session = Depends(get_session)):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

#List books with optional filters
@router.get("/", response_model=List[Book])
def list_books(
    author: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    statement = select(Book)

    if author:
        statement = statement.where(Book.author.ilike(f"%{author}%"))
    if title:
        statement = statement.where(Book.title.ilike(f"%{title}%"))

    return session.exec(statement).all()

#Get, update, and delete a book by ID
@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

#Update a book
@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, updated: Book, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = updated.title
    book.author = updated.author
    book.year = updated.year

    session.add(book)
    session.commit()
    session.refresh(book)
    return book

#Delete a book
@router.delete("/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(book)
    session.commit()
    return {"message": "Book deleted"}