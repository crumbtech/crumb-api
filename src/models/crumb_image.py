import sqlalchemy as sa

from .base import TrackedTableMixin, BaseModel


UPLOAD_STATUSES = dict(
    UPLOADING='uploading',
    SUCCESS='success',
    ERROR='error')


class CrumbImage(TrackedTableMixin, BaseModel):
    __tablename__ = 'crumb_images'
    id = sa.Column(sa.Integer, primary_key=True)
    crumb_id = sa.Column(sa.Integer, sa.ForeignKey('crumbs.id'),
                         nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    s3_url = sa.Column(sa.Text, nullable=False)
    upload_status = sa.Column(sa.Enum(UPLOAD_STATUSES['UPLOADING'],
                                      UPLOAD_STATUSES['SUCCESS'],
                                      UPLOAD_STATUSES['ERROR'],
                                      name='crumb_image_upload_statuses'),
                              nullable=False,
                              default=UPLOAD_STATUSES['UPLOADING'])

    crumb = sa.orm.relationship('Crumb')
    user = sa.orm.relationship('User')
