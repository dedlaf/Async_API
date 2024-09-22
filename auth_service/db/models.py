import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Text, UniqueConstraint, text
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
    login_histories = relationship(
        "LoginHistory", back_populates="user", cascade="delete, merge, save-update"
    )


class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False, unique=True)


def create_partition_for_login_history(target, connection, **kw) -> None:
    connection.execute(
        text(
            """CREATE TABLE IF NOT EXISTS "auth"."login_history_in_smart"  PARTITION OF "auth"."login_history" FOR VALUES IN ('smart')"""
        )
    )
    connection.execute(
        text(
            """CREATE TABLE IF NOT EXISTS "auth"."login_history_in_mobile" PARTITION OF "auth"."login_history" FOR VALUES IN ('mobile')"""
        )
    )
    connection.execute(
        text(
            """CREATE TABLE IF NOT EXISTS "auth"."login_history_in_web" PARTITION OF "auth"."login_history" FOR VALUES IN ('web')"""
        )
    )


class LoginHistory(Base):
    __tablename__ = "login_history"
    __table_args__ = (
        UniqueConstraint("id", "user_device_type"),
        {
            "postgresql_partition_by": "LIST (user_device_type)",
            "listeners": [("after_create", create_partition_for_login_history)],
            "schema": "auth",
        },
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.user.id"), nullable=False)
    logged_in_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_agent = Column(Text)
    user_device_type = Column(Text, primary_key=True)

    user = relationship("User", back_populates="login_histories")

    def __repr__(self) -> str:
        return f"<LoginHistory {self.user_id}:{self.logged_in_at}>"
