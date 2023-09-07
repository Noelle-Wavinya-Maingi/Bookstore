"""Added total_sales colum to the Book

Revision ID: 977d5bb3bcfb
Revises: 8cebdb5fdf33
Create Date: 2023-09-06 22:47:01.975470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '977d5bb3bcfb'
down_revision = '8cebdb5fdf33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('books', sa.Column('total_sales', sa.Integer(), nullable = True))

def downgrade() -> None:
    op.drop_column('books', 'total_sales')
