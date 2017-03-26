"""create crumbs table

Revision ID: cfb3bc5de4a6
Revises:
Create Date: 2017-03-26 16:15:32.870108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfb3bc5de4a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('crumbs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('status', sa.Enum('active', 'ended',
                              name='crumb_statuses'), nullable=True),
                    sa.Column('date_created', sa.DateTime(), nullable=False),
                    sa.Column('date_modified', sa.DateTime(), nullable=False))


def downgrade():
    op.drop_table('crumbs')
