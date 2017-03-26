"""create crumbs table

Revision ID: 78d19b951526
Revises:
Create Date: 2017-03-26 14:09:56.282376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78d19b951526'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('crumbs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('date_created', sa.DateTime(), nullable=False),
                    sa.Column('date_modified', sa.DateTime(), nullable=False))


def downgrade():
    op.drop_table('crumbs')
