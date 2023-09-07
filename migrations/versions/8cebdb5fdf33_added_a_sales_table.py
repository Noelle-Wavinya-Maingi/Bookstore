"""Added a sales table

Revision ID: 8cebdb5fdf33
Revises: aaa733d1226f
Create Date: 2023-09-06 22:02:32.664005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cebdb5fdf33'
down_revision = 'aaa733d1226f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'sales',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id'), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable = True),
        sa.Column('total_amount', sa.Float(), nullable = True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('sales')