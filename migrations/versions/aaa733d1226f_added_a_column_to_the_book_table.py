"""Added a column to the Book table

Revision ID: aaa733d1226f
Revises: d078e58968c4
Create Date: 2023-09-06 21:56:34.049151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaa733d1226f'
down_revision = 'd078e58968c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('books', sa.Column('inventory', sa.Integer(), nullable = True))
    op.add_column('books', sa.Column('price', sa.Float(), nullable = True))

def downgrade() -> None:
    op.drop_column('books', 'inventory')
    op.drop_column('books', 'price')
