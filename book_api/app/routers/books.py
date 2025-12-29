from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas import Book, BookCreate
from app import crud

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=Book)
def create(book: BookCreate):
    return crud.create_book(book)

@router.get("/", response_model=List[Book])
def list_books(
    author: Optional[str] = Query(None),
    title: Optional[str] = Query(None)
):
    books = crud.get_all_books()

    if author:
        books = [b for b in books if b.author.lower() == author.lower()]

    if title:
        books = [b for b in books if title.lower() in b.title.lower()]

    return books


@router.put("/{book_id}", response_model=Book)
def update(book_id: int, updated_book: BookCreate):
    book = crud.update_book(book_id, updated_book)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{book_id}", response_model=Book)
def get(book_id: int):
    book = crud.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}")
def delete(book_id: int):
    if not crud.delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}
