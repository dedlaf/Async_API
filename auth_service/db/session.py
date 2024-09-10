from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config.components.settings import (DB_HOST, DB_NAME, DB_PASSWORD,
                                             DB_USER)

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
