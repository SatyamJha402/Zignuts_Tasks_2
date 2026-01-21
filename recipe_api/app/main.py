from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import auth, recipes

app = FastAPI()

#Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#Include routers
app.include_router(auth.router)
app.include_router(recipes.router)

#Basic root endpoint
@app.get("/")
def root():
    return {"message": "Recipe API is running"}