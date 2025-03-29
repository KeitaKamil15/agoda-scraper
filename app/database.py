from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL database URL
DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost/mydatabase"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session maker to handle database connections
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for defining database models
Base = declarative_base()

def get_db():
    """
    Dependency to get the database session.
    Ensures the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
