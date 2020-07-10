"""create QuestionPicture Table

Revision ID: 9fc197fe2ae6
Revises: 3965904bd4dd
Create Date: 2020-07-08 20:15:09.902925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9fc197fe2ae6"
down_revision = "3965904bd4dd"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "question_pictures",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column(
            "question_id", sa.Integer, sa.ForeignKey("questions.id"), nullable=False
        ),
    )


def downgrade():
    op.drop_table("question_pictures")
