from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import users, books

app = FastAPI()

# Create database tables on startup
@app.on_event("startup")
def startup():
    create_db_and_tables()

#Include routers
app.include_router(users.router)
app.include_router(books.router)