from graphene import ObjectType, ID, String, Field, List, Argument, Schema

from src.database import db_session
from src.models import Crumb as CrumbModel
from src.models import CrumbImage as CrumbImageModel


class Crumb(ObjectType):
    id = ID()
    status = Field(String)


class CrumbImage(ObjectType):
    id = ID()
    upload_status = Field(String)
    s3_url = Field(String)


class Query(ObjectType):
    all_crumbs = Field(List(Crumb))
    crumb_images = Field(List(CrumbImage), crumb_id=Argument(ID))

    def resolve_all_crumbs(self, args, context, info):
        with db_session() as session:
            res = session.query(CrumbModel)
            return [Crumb(id=crumb.id, status=crumb.status)
                    for crumb in res]

    def resolve_crumb_images(self, args, context, info):
        with db_session() as session:
            res = session.query(CrumbImageModel).filter_by(
                crumb_id=args['crumb_id'])
            return [CrumbImage(id=crumb_image.id,
                               upload_status=crumb_image.upload_status,
                               s3_url=crumb_image.s3_url)
                    for crumb_image in res]


schema = Schema(query=Query)
