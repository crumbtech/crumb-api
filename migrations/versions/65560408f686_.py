""" adds password salt to users table

Revision ID: 65560408f686
Revises: 88e4596adbda
Create Date: 2017-04-10 22:26:26.044564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65560408f686'
down_revision = '88e4596adbda'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column(
        'password_salt', sa.Text(), nullable=False))


def downgrade():
    op.drop_column('users', 'password_salt')
