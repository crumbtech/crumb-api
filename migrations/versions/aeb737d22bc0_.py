""" adds first and last name to users

Revision ID: aeb737d22bc0
Revises: 421166f60a61
Create Date: 2017-04-13 20:17:08.761551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aeb737d22bc0'
down_revision = '421166f60a61'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('first_name', sa.Text(), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.Text(), nullable=False))


def downgrade():
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
