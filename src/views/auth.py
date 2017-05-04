import urllib

from flask import Blueprint, make_response, jsonify, request, g, current_app

from src.models import User
from src.database import db_session
from src.lib import normalize_phone_number, generate_presigned_image_upload_url

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    post_data = request.get_json()
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    phone_number = post_data.get('phone_number')
    normalized_phone = normalize_phone_number(phone_number)
    with db_session() as session:
        existing = session.query(User).filter_by(
            phone_number=normalized_phone).first()
        if existing:
            return make_response(jsonify({
                'message': 'already-exists',
            })), 202
        else:
            user = User(first_name=first_name, last_name=last_name,
                        phone_number=phone_number)
            session.add(user)
            session.commit()
            user.send_confirmation_code()
            return make_response(jsonify({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_id': str(user.id),
            })), 200


@auth.route('/login', methods=['POST'])
def login():
    post_data = request.get_json()
    phone_number = post_data.get('phone_number')
    normalized_phone = normalize_phone_number(phone_number)
    with db_session() as session:
        user = session.query(User).filter_by(
            phone_number=normalized_phone).first()
        if user:
            user.send_confirmation_code()
            return make_response(jsonify({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_id': str(user.id),
            })), 200

        else:
            return make_response(jsonify({
                'message': 'no-user-for-phone',
            })), 401


@auth.route('/confirm', methods=['POST'])
def confirm():
    post_data = request.get_json()
    user_id = post_data.get('user_id')
    confirmation_code = post_data.get('confirmation_code')
    with db_session() as session:
        user = session.query(User).filter_by(id=user_id).one()
        user.confirm_phone_number_with_code(confirmation_code)
        session.add(user)
        session.commit()
        if user.phone_number_confirmed:
            return make_response(jsonify({
                'auth_token': user.generate_auth_token(),
            })), 200
        else:
            return make_response(jsonify({
                'message': 'invalid-code',
            })), 401


@auth.route('/current-user', methods=['GET'])
def get_current_user_from_auth_header():
    return make_response(jsonify(g.current_user)), 200


@auth.route('/presigned-image-upload-url', methods=['GET'])
def get_presigned_image_upload_url():
    """
    returns a presigned url to be used by client to create an s3 object.
    also returns the s3 url where that object can be accessed once created.
    """
    if g.current_user:
        extension = request.args.get('extension', '.jpg')
        presigned_url = generate_presigned_image_upload_url(
                g.current_user['id'], extension=extension)

        return make_response(jsonify({
            'presigned_url': presigned_url,
            's3_url': urllib.parse.splitquery(presigned_url)[0],
        })), 200
    else:
        return make_response(jsonify({
            'message': 'authentication-required',
        })), 401
