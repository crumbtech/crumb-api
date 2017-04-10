from flask import Blueprint, make_response, jsonify

import src.models as models
import src.database as db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    post_data = request.get_json()
    user = models.User()
    with db.session_manager() as session:
        session.add(user)
        session.commit()
        # instance of user model is now synced with db
        auth_token = user.generate_auth_token()

    return make_response(jsonify({'auth_token': auth_token}))
