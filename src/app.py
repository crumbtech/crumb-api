def create_app(config_object='src.config.for_env'):
    from flask import Flask
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_object)

    from flask_graphql import GraphQLView
    import src.schema as schema
    import src.views as views
    import src.extensions as extensions

    current_user = extensions.CurrentUser()
    current_user.init_app(flask_app)

    flask_app.register_blueprint(views.auth, url_prefix='/auth')

    graphiql_enabled = flask_app.config.get('GRAPHIQL')
    flask_app.add_url_rule('/graphql',
                           view_func=GraphQLView.as_view(
                               'graphql',
                               schema=schema.schema,
                               graphiql=graphiql_enabled))

    return flask_app
