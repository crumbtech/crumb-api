import datetime as dt
import sqlalchemy as sa

Base = sa.ext.declarative.declarative_base()


class BaseModel(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    date_created = sa.Column(sa.DateTime, nullable=False,
                             default=dt.datetime.utcnow)
    date_modified = sa.Column(sa.DateTime, nullable=False,
                              default=dt.datetime.utcnow,
                              onupdate=dt.datetime.utcnow)
