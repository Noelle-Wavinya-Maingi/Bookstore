"""Created Users table

Revision ID: 0fa77c3040fb
Revises: 5beefdf1128f
Create Date: 2023-09-06 12:43:05.224867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa77c3040fb'
down_revision = '5beefdf1128f'
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