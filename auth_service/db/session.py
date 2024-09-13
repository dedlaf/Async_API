from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config.components.settings import Settings

settings = Settings()

DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_function() -> Session:
    return SessionLocal()
