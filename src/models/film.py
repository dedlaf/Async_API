from sqlalchemy import Column, Text, Date, Float, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid


Base = declarative_base()


class Film(Base):
    __tablename__ = 'film'
    __table_args__ = (
        UniqueConstraint('id'),
        {'schema': 'content'},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text)
    creation_date = Column(Date)
    rating = Column(Float)
    type = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True))
    modified = Column(TIMESTAMP(timezone=True))

    genres = relationship('Genre', secondary='content.genre_film', back_populates='films')
    persons = relationship('Person', secondary='content.person_film', back_populates='films')


class Genre(Base):
    __tablename__ = 'genre'
    __table_args__ = (
        UniqueConstraint('id'),
        {'schema': 'content'},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text)
    created = Column(TIMESTAMP(timezone=True))
    modified = Column(TIMESTAMP(timezone=True))

    films = relationship('FilmWork', secondary='content.genre_film', back_populates='genres')


class GenreFilm(Base):
    __tablename__ = 'genre_film'
    __table_args__ = (
        UniqueConstraint('id', 'film_id', 'genre_id', name='unique_film_genre_role_idx'),
        {'schema': 'content'},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    genre_id = Column(UUID(as_uuid=True), ForeignKey('content.genre.id'), nullable=False)
    film_id = Column(UUID(as_uuid=True), ForeignKey('content.film.id'), nullable=False)
    created = Column(TIMESTAMP(timezone=True))


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = (
        UniqueConstraint('id'),
        {'schema': 'content'},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True))
    modified = Column(TIMESTAMP(timezone=True))

    films = relationship('FilmWork', secondary='content.person_film', back_populates='persons')


class PersonFilmWork(Base):
    __tablename__ = 'person_film'
    __table_args__ = (
        UniqueConstraint('id', 'film_id', 'person_id', 'role', name='film_person_role_idx'),
        {'schema': 'content'},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey('content.person.id'), nullable=False)
    film_id = Column(UUID(as_uuid=True), ForeignKey('content.film.id'), nullable=False)
    role = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True))
