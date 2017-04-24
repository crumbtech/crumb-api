import sqlalchemy as sa

from .base import TrackedTableMixin, BaseModel


class CrumbImage(TrackedTableMixin, BaseModel):
    __tablename__ = 'crumb_images'
    id = sa.Column(sa.Integer, primary_key=True)
    crumb_id = sa.Column(sa.Integer, sa.ForeignKey('crumbs.id'),
                         nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    s3_url = sa.Column(sa.Text, nullable=False)

    crumb = sa.orm.relationship('Crumb')
    user = sa.orm.relationship('User')
