"""empty message

Revision ID: 0ec9adcec84d
Revises:
Create Date: 2017-03-27 23:49:49.607146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ec9adcec84d'
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
    pass
