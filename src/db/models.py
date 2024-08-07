import uuid

from sqlalchemy import (TIMESTAMP, Column, Date, Float, ForeignKey, String,
                        Text, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class FilmWork(Base):
    __tablename__ = "film_work"
    __table_args__ = (
        UniqueConstraint("id"),
        {"schema": "content"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text)
    creation_date = Column(Date)
    rating = Column(Float)
    type = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True))
    modified = Column(TIMESTAMP(timezone=True))
    certificate = Column(String(512), nullable=True)
    file_path = Column(String(512), nullable=True)

    genres = relationship(
        "Genre", secondary="content.genre_film_work", back_populates="film_works"
    )
    persons = relationship(
        "Person", secondary="content.person_film_work", back_populates="film_works"
    )


class Genre(Base):
    __tablename__ = "genre"
    __table_args__ = (
        UniqueConstraint("id"),
        {"schema": "content"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text)
    created = Column(TIMESTAMP(timezone=True))
    modified = Column(TIMESTAMP(timezone=True))

    film_works = relationship(
        "FilmWork", secondary="content.genre_film_work", back_populates="genres"
    )


class GenreFilmWork(Base):
    __tablename__ = "genre_film_work"
    __table_args__ = (
        UniqueConstraint(
            "id", "film_work_id", "genre_id", name="unique_film_work_genre_role_idx"
        ),
        {"schema": "content"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    genre_id = Column(
        UUID(as_uuid=True), ForeignKey("content.genre.id"), nullable=False
    )
    film_work_id = Column(
        UUID(as_uuid=True), ForeignKey("content.film_work.id"), nullable=False
    )
    created = Column(TIMESTAMP(timezone=True))


class Person(Base):
    __tablename__ = "person"
    __table_args__ = (
        UniqueConstraint("id"),
        {"schema": "content"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True))
    modified = Column(TIMESTAMP(timezone=True))

    film_works = relationship(
        "FilmWork", secondary="content.person_film_work", back_populates="persons"
    )


class PersonFilmWork(Base):
    __tablename__ = "person_film_work"
    __table_args__ = (
        UniqueConstraint(
            "id", "film_work_id", "person_id", "role", name="film_work_person_role_idx"
        ),
        {"schema": "content"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(
        UUID(as_uuid=True), ForeignKey("content.person.id"), nullable=False
    )
    film_work_id = Column(
        UUID(as_uuid=True), ForeignKey("content.film_work.id"), nullable=False
    )
    role = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True))
