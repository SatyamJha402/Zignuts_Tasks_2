from pydantic import BaseModel

#the models for the book data
class BookBase(BaseModel):
    title: str
    author: str
    year: int
    
#the model for creating a new book
class BookCreate(BookBase):
    pass

#the model for returning book data with an ID
class Book(BookBase):
    id: int