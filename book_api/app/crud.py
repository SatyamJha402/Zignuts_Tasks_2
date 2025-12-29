from typing import List
from app.schemas import Book, BookCreate

books: List[Book] = []

#Create a new book
def create_book(book: BookCreate) -> Book:
    book_id = len(books) + 1
    new_book = Book(id=book_id, **book.dict())
    books.append(new_book)
    return new_book

#Get all books
def get_all_books():
    return books

#Update a book by ID
def update_book(book_id: int, updated_book: BookCreate):
    for index, book in enumerate(books):
        #Update the book if the ID matches
        if book.id == book_id:
            books[index] = Book(id=book_id, **updated_book.dict())
            return books[index]
    return None

#Get a book by ID
def get_book_by_id(book_id: int):
    for book in books:
        #Return the book if the ID matches
        if book.id == book_id:
            return book
    return None

#Delete a book by ID
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return True
    return False