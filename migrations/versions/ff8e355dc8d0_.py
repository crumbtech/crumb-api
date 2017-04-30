""" creates crumb_images table

Revision ID: ff8e355dc8d0
Revises: 49cad5f3dfc0
Create Date: 2017-04-24 15:35:04.989447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff8e355dc8d0'
down_revision = '49cad5f3dfc0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('crumb_images',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('crumb_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(['crumb_id'], ['crumbs.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.Column('s3_url', sa.Text(), nullable=False),
                    sa.Column(
                        'upload_status',
                        sa.Enum(
                            'uploading',
                            'success',
                            'failed',
                            name='crumb_image_upload_statuses'),
                        nullable=False),
                    sa.Column('date_created', sa.DateTime(), nullable=False),
                    sa.Column('date_modified', sa.DateTime(), nullable=False))


def downgrade():
    op.drop_table('crumb_items')
