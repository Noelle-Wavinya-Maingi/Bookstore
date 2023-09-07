"""Add the purchase_time column.

Revision ID: ec79702edcf0
Revises: 977d5bb3bcfb
Create Date: 2023-09-07 16:47:13.354301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec79702edcf0'
down_revision = '977d5bb3bcfb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('sales', sa.Column('purchase_time', sa.DateTime(), nullable = True))
   
def downgrade() -> None:
    op.drop_column('sales', 'purchase_time')