from pydantic import BaseModel

#the models for the book data
class BookBase(BaseModel):
    title: str
    author: str
    year: int
    
class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int