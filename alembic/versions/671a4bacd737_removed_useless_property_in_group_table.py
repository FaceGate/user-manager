"""Removed useless property in group table

Revision ID: 671a4bacd737
Revises: 693d47d886c7
Create Date: 2019-07-21 18:21:52.606873

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "671a4bacd737"
down_revision = "693d47d886c7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("groups", "expiration_date", schema="user_manager")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "groups",
        sa.Column(
            "expiration_date",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        schema="user_manager",
    )
    # ### end Alembic commands ###
