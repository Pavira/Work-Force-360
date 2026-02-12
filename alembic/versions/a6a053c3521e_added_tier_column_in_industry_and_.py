"""Added tier column in industry and category table

Revision ID: a6a053c3521e
Revises: 06049b45ae4c
Create Date: 2026-02-12 14:04:50.199002

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a6a053c3521e"
down_revision: Union[str, Sequence[str], None] = "06049b45ae4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1️⃣ Add tier to industry_types
    op.add_column(
        "industry_types",
        sa.Column("tier", sa.String(length=50), nullable=True),
    )

    # 2️⃣ Add tier to category_skills
    op.add_column(
        "category_skills",
        sa.Column("tier", sa.String(length=50), nullable=True),
    )

    # 4️⃣ Create FK
    op.create_foreign_key(
        "fk_category_skills_tier",
        "category_skills",
        "industry_types",
        ["tier"],
        ["tier"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_constraint("fk_category_skills_tier", "category_skills", type_="foreignkey")
    op.drop_column("category_skills", "tier")
    op.drop_column("industry_types", "tier")

    # ### end Alembic commands ###
