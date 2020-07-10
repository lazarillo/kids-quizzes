"""create Question table

Revision ID: 3965904bd4dd
Revises: 7641df155b93
Create Date: 2020-07-08 19:38:08.522663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3965904bd4dd"
down_revision = "7641df155b93"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("header", sa.Unicode(100), nullable=False),
        sa.Column("details", sa.Text, nullable=True),
        sa.Column("creator_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade():
    op.drop_table("questions")
