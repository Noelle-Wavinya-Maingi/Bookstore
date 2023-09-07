"""Added the arrears column in the fines table

Revision ID: 5a924562f3f7
Revises: ec79702edcf0
Create Date: 2023-09-18 19:53:43.288687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a924562f3f7'
down_revision = 'ec79702edcf0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('fines', sa.Column('arrears', sa.Boolean(), nullable = True))
   
def downgrade() -> None:
    op.drop_column('fines', 'arrears')