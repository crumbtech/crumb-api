from flask import Blueprint, make_response, jsonify, request

import src.models as models
import src.database as db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    post_data = request.form
    user = models.User(
        phone_number=post_data.get('phone_number'),
        password=post_data.get('password'))
    with db.session_manager() as session:
        session.add(user)
        session.commit()
        # instance of user model is now synced with db
        auth_token = user.generate_auth_token()

    return make_response(jsonify({'auth_token': auth_token}))
