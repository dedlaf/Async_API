"""Initial migration

Revision ID: fb354b2e6a4e
Revises: 
Create Date: 2024-08-03 07:24:03.542730

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fb354b2e6a4e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "film_work",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("creation_date", sa.Date(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("type", sa.Text(), nullable=False),
        sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("modified", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("certificate", sa.String(length=512), nullable=True),
        sa.Column("file_path", sa.String(length=512), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        schema="content",
    )
    op.create_table(
        "genre",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("modified", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        schema="content",
    )
    op.create_table(
        "person",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("full_name", sa.Text(), nullable=False),
        sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("modified", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        schema="content",
    )
    op.create_table(
        "genre_film_work",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("genre_id", sa.UUID(), nullable=False),
        sa.Column("film_work_id", sa.UUID(), nullable=False),
        sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["film_work_id"],
            ["content.film_work.id"],
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["content.genre.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "id", "film_work_id", "genre_id", name="unique_film_work_genre_role_idx"
        ),
        schema="content",
    )
    op.create_table(
        "person_film_work",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("person_id", sa.UUID(), nullable=False),
        sa.Column("film_work_id", sa.UUID(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["film_work_id"],
            ["content.film_work.id"],
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["content.person.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "id", "film_work_id", "person_id", "role", name="film_work_person_role_idx"
        ),
        schema="content",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("person_film_work", schema="content")
    op.drop_table("genre_film_work", schema="content")
    op.drop_table("person", schema="content")
    op.drop_table("genre", schema="content")
    op.drop_table("film_work", schema="content")
    # ### end Alembic commands ###
