""" adds unique constraint to phone number column

Revision ID: 421166f60a61
Revises: 65560408f686
Create Date: 2017-04-10 23:46:41.506578

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '421166f60a61'
down_revision = '88e4596adbda'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'users', ['phone_number'])


def downgrade():
    op.drop_constraint(None, 'users', type_='unique')
