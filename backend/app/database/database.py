"""
SQLAlchemy database setup supporting SQLite (default) and PostgreSQL migration.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

DB_DIR = Path(__file__).parent.parent.parent
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_DIR}/trip_planner.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import db_models
    Base.metadata.create_all(bind=engine)
    print("[OK] Database initialized")
