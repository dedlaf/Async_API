import uuid

from sqlalchemy import (Column, Text, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text)
    role_id = Column(UUID, ForeignKey('auth.role.id'))

    role = relationship("Role", backref="users")


class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
