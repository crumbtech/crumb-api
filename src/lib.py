import jwt

import src.config as config
cfg = config.config_for_env


def encode_jwt_token(payload):
    return jwt.encode(payload, cfg.JWT_SECRET, algorithm='HS256')


def encode_jwt_token_for_subject(sub):
    payload = {'sub': sub}
    return encode_jwt_token(payload)


def decode_jwt_token(token):
    return jwt.decode(token, cfg.JWT_SECRET)
