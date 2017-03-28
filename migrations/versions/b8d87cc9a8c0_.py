"""create crumbs table

Revision ID: b8d87cc9a8c0
Revises:
Create Date: 2017-03-27 23:33:52.407631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8d87cc9a8c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('crumbs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('date_created', sa.DateTime(), nullable=False),
                    sa.Column('date_modified', sa.DateTime(), nullable=False),
                    sa.Column('status',
                              sa.Enum('active',
                                      'ended',
                                      name='crumb_statuses'),
                              nullable=False))


def downgrade():
    op.drop_table('crumbs')
