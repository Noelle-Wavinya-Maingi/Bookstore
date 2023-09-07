"""Created books table

Revision ID: 4bbeb88605e4
Revises: de4c8ed3f7be
Create Date: 2023-09-06 12:57:31.499826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bbeb88605e4'
down_revision = 'de4c8ed3f7be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('author', sa.String(), nullable = True),
        sa.Column('status', sa.Boolean(), nullable = True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('books')