from flask import Blueprint, make_response, jsonify, request, g

import src.models as models
import src.database as db
import src.lib as lib

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    post_data = request.get_json()
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    phone_number = post_data.get('phone_number')
    password = post_data.get('password')
    normalized_phone = lib.normalize_phone_number(phone_number)
    with db.session_manager() as session:
        existing = session.query(models.User).filter_by(
            phone_number=normalized_phone).first()
        if existing:
            return make_response(jsonify({
                'status': 'already-exists',
            })), 202
        else:
            user = models.User(first_name=first_name, last_name=last_name,
                               phone_number=phone_number, password=password)
            session.add(user)
            session.commit()
            auth_token = user.generate_auth_token()
            return make_response(jsonify({
                'auth_token': auth_token,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })), 200


@auth.route('/login', methods=['POST'])
def login():
    post_data = request.get_json()
    phone_number = post_data.get('phone_number')
    password = post_data.get('password')
    normalized_phone = lib.normalize_phone_number(phone_number)
    with db.session_manager() as session:
        existing = session.query(models.User).filter_by(
            phone_number=normalized_phone).first()
        if existing:
            if existing.verify_password(password):
                auth_token = existing.generate_auth_token()
                return make_response(jsonify({
                    'auth_token': auth_token,
                })), 200
            else:
                return make_response(jsonify({
                    'status': 'invalid-password',
                })), 401

        else:
            return make_response(jsonify({
                'status': 'no-user-for-phone',
            })), 401


@auth.route('/current-user', methods=['GET'])
def get_current_user_from_auth_header():
    return make_response(jsonify(g.current_user)), 200
