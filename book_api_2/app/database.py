from sqlmodel import SQLModel, create_engine, Session
from app.config import DATABASE_URL

DATABASE_URL = DATABASE_URL

#Create the database engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

#Create the database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Dependency to get a session
def get_session():
    with Session(engine) as session:
        yield session