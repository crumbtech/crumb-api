""" adds confirmation code to users table

Revision ID: 49cad5f3dfc0
Revises: aeb737d22bc0
Create Date: 2017-04-17 14:23:55.068224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49cad5f3dfc0'
down_revision = 'aeb737d22bc0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('confirmation_code', sa.Text(),
                                     nullable=False))
    op.add_column('users', sa.Column('phone_number_confirmed', sa.Boolean(),
                                     nullable=False))


def downgrade():
    op.drop_column('users', 'phone_number_confirmed')
    op.drop_column('users', 'confirmation_code')
