import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()


class TrackedTableMixin(object):
    date_created = sa.Column(sa.DateTime, nullable=False,
                             default=dt.datetime.utcnow)
    date_modified = sa.Column(sa.DateTime, nullable=False,
                              default=dt.datetime.utcnow,
                              onupdate=dt.datetime.utcnow)
