"""Add user_id to todos

Revision ID: 6c4a8e7b1d21
Revises: f798d63648b2
Create Date: 2026-03-12 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6c4a8e7b1d21"
down_revision: Union[str, None] = "f798d63648b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("user_id", sa.String(), nullable=True))
    op.create_index(op.f("ix_todos_user_id"), "todos", ["user_id"], unique=False)
    op.create_foreign_key(
        "fk_todos_user_id_users",
        "todos",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_todos_user_id_users", "todos", type_="foreignkey")
    op.drop_index(op.f("ix_todos_user_id"), table_name="todos")
    op.drop_column("todos", "user_id")
