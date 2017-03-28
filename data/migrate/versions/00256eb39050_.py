"""create crumbs table

Revision ID: 00256eb39050
Revises:
Create Date: 2017-03-27 22:33:27.469917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00256eb39050'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('crumbs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('status',
                              sa.Enum('active',
                                      'ended',
                                      name='crumb_statuses'),
                              nullable=False),
                    sa.Column('date_created', sa.DateTime(), nullable=False),
                    sa.Column('date_modified', sa.DateTime(), nullable=False))


def downgrade():
    op.drop_table('crumbs')
