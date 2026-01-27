from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import users, books
import time
from fastapi import Request

app = FastAPI()

# Create database tables on startup
@app.on_event("startup")
def startup():
    create_db_and_tables()

#Include routers
app.include_router(users.router, prefix="/auth", tags=["Auth"])
app.include_router(books.router, prefix="/books", tags=["Books"])


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    print(
        f"{request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.4f}s"
    )

    return response