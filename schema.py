import graphene

import crumb_api.database as db
import crumb_api.models as models


class Crumb(graphene.ObjectType):
    id = graphene.ID()
    status = graphene.Field(graphene.String)


class Query(graphene.ObjectType):
    all_crumbs = graphene.Field(graphene.List(Crumb))

    def resolve_all_crumbs(self, args, context, info):
        with db.session_manager() as session:
            res = session.query(models.Crumb)
            return [Crumb(id=instance.id, status=instance.status)
                    for instance in res]


schema = graphene.Schema(query=Query)
