"""Created borrowed_books table

Revision ID: d9cdc7d0690b
Revises: 4bbeb88605e4
Create Date: 2023-09-06 13:07:49.053368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9cdc7d0690b'
down_revision = '4bbeb88605e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'borrowed_books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'),nullable = True),
        sa.Column('return_date', sa.DateTime(), nullable = True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('borrowed_books')