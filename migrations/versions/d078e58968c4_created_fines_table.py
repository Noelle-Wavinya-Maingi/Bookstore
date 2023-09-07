"""Created fines  table

Revision ID: d078e58968c4
Revises: d9cdc7d0690b
Create Date: 2023-09-06 17:15:47.547868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd078e58968c4'
down_revision = 'd9cdc7d0690b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'fines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'),nullable = True),
        sa.Column('amount', sa.Float(), nullable = True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('fines')