"""Database utilities."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import Settings

settings = Settings()

# In production, prefer PostgreSQL URL via env. SQLite is kept for local runs.
engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def get_session():
    """Yield a SQLAlchemy session; suitable for FastAPI dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

