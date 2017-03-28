from flask import Flask


def create_app(config_object='src.config.config_for_env'):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_object)

    from flask_graphql import GraphQLView
    import src.schema as schema

    graphiql_enabled = flask_app.config.get('GRAPHIQL')

    flask_app.add_url_rule('/graphql',
                           view_func=GraphQLView.as_view(
                               'graphql',
                               schema=schema.schema,
                               graphiql=graphiql_enabled))
    return flask_app
