from flask import Flask
from flask_graphql import GraphQLView

import src.schema as schema

flask_app = Flask(__name__)

flask_app.add_url_rule('/graphql',
                 view_func=GraphQLView.as_view('graphql',
                                               schema=schema.schema,
                                               graphiql=True))
