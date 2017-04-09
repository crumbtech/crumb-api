"""create users table

Revision ID: d386d3919523
Revises: 39ad0c116ba2
Create Date: 2017-04-09 13:41:39.132318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd386d3919523'
down_revision = '39ad0c116ba2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('date_created', sa.DateTime(), nullable=False),
                    sa.Column('date_modified', sa.DateTime(), nullable=False))


def downgrade():
    op.drop_table('users')
