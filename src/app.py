def create_app(config_object='src.config.config_for_env'):
    from flask import Flask, request, g
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_object)

    from flask_graphql import GraphQLView
    import src.schema as schema
    import src.views as views
    import src.models as models
    import src.database as db

    @flask_app.before_request
    def before_request():
        g.current_user = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        user_id = models.User.decode_auth_token(auth_token)
        if user_id:
            with db.session_manager() as session:
                user = session.query(models.User).filter_by(id=user_id).one()
                g.current_user = dict(
                    id=user.id,
                    phone_number=user.phone_number,
                )

    flask_app.register_blueprint(views.auth, url_prefix='/auth')

    graphiql_enabled = flask_app.config.get('GRAPHIQL')
    flask_app.add_url_rule('/graphql',
                           view_func=GraphQLView.as_view(
                               'graphql',
                               schema=schema.schema,
                               graphiql=graphiql_enabled))

    return flask_app
