import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    role_id = Column(UUID, ForeignKey("auth.role.id"), nullable=True)

    role = relationship("Role", backref="users")


class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False, unique=True)


class LoginHistory(Base):
    __tablename__ = "login_history"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("auth.user.id"), nullable=True)
    logged_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", backref="login_histories")
