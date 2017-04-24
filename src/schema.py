import graphene

from src.database import db_session
from src.models.crumb import Crumb as CrumbModel


class Crumb(graphene.ObjectType):
    id = graphene.ID()
    status = graphene.Field(graphene.String)


class Query(graphene.ObjectType):
    all_crumbs = graphene.Field(graphene.List(Crumb))

    def resolve_all_crumbs(self, args, context, info):
        with db_session() as session:
            res = session.query(CrumbModel)
            return [Crumb(id=instance.id, status=instance.status)
                    for instance in res]


schema = graphene.Schema(query=Query)
