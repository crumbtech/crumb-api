""" add phone number and password to users table

Revision ID: 88e4596adbda
Revises: d386d3919523
Create Date: 2017-04-10 02:46:54.129717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88e4596adbda'
down_revision = 'd386d3919523'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('password', sa.Text(), nullable=False))
    op.add_column('users', sa.Column('phone_number', sa.Text(),
                                     nullable=False))


def downgrade():
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'password')
