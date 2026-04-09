"""Add fcm_token column to workers

Revision ID: f3a1c5b2d9e0
Revises: 3185d836784c
Create Date: 2026-04-06 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3a1c5b2d9e0"
down_revision: Union[str, Sequence[str], None] = "3185d836784c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("workers", sa.Column("fcm_token", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("workers", "fcm_token")
