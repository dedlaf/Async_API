import uuid

from sqlalchemy import (Column, Text, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint("id"),
        {"schema": "auth"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text)

