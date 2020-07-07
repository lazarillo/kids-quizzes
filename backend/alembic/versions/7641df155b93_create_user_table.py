"""create User table

Revision ID: 7641df155b93
Revises: 
Create Date: 2020-07-07 23:12:47.560253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7641df155b93"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.Unicode(50), nullable=False),
        sa.Column("username", sa.Unicode(50), unique=True, nullable=False, index=True),
        sa.Column("email", sa.Unicode(100), nullable=True),
        sa.Column("hashed_password", sa.Unicode(50), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, default=True),
    )


def downgrade():
    op.drop_table("users")