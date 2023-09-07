"""Created Users table

Revision ID: de4c8ed3f7be
Revises: 59020caf5446
Create Date: 2023-09-06 12:48:30.610721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de4c8ed3f7be'
down_revision = '59020caf5446'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('users')