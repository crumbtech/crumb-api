from flask import request, g

import src.models as models
import src.database as db


class CurrentUser(object):
    def init_app(self, app):
        @app.before_request
        def get_current_user():
            g.current_user = None
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''
            user_id = models.User.decode_user_id_from_auth_token(auth_token)
            if user_id:
                with db.session_manager() as session:
                    user = session.query(models.User).get(user_id)
                    if user.phone_number_confirmed:
                        g.current_user = dict(id=user.id,
                                              first_name=user.first_name,
                                              last_name=user.last_name)
