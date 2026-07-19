"""
Database engine + session factory. Call init_db() once at app startup
(app.py does this) to create tables if they don't exist yet.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from database.models import Base

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    """Create all tables. Safe to call multiple times."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a DB session; use as a context manager in modules."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()