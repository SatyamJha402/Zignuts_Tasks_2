from sqlmodel import SQLModel, create_engine, Session
from app.config import DATABASE_URL

DATABASE_URL = DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session

# Initialize the database
def init_db():
    from app.models import User, Company, Job, Tag, JobTag
    SQLModel.metadata.create_all(engine)