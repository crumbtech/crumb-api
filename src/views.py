from flask import Blueprint, make_response, jsonify, request

import src.models as models
import src.database as db
import src.lib as lib

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    post_data = request.get_json()
    phone_number = post_data.get('phone_number')
    password = post_data.get('password')
    normalized_phone = lib.normalize_phone_number(phone_number)
    with db.session_manager() as session:
        existing = session.query(models.User).filter_by(
            phone_number=normalized_phone).first()
        if existing:
            return make_response(jsonify({
                'status': 'phone number already in use',
            })), 202
        else:
            user = models.User(phone_number=phone_number, password=password)
            session.add(user)
            session.commit()
            auth_token = user.generate_auth_token()
            return make_response(jsonify({
                'auth_token': auth_token,
            })), 200
