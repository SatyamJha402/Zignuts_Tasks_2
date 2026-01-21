from fastapi import FastAPI
from app.database import init_db
from app.routers import auth, company, jobs

app = FastAPI(title="Job Board API")
app.include_router(auth.router)
app.include_router(company.router)
app.include_router(jobs.router)

#Initialize the database
@app.on_event("startup")
def on_startup():
    init_db()