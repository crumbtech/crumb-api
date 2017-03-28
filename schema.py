import graphene

from data.database import session_manager
import data.models as models


class Crumb(graphene.ObjectType):
    id = graphene.ID()
    status = graphene.Field(graphene.String)


class Query(graphene.ObjectType):
    all_crumbs = graphene.Field(graphene.List(Crumb))
    crumb = graphene.Field(Crumb)

    def resolve_all_crumbs(self, args, context, info):
        with session_manager() as session:
            res = session.query(models.Crumb)
            return [Crumb(id=instance.id, status=instance.status)
                    for instance in res]


schema = graphene.Schema(query=Query)
