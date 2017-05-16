import os


class Config(object):
    CRUMB_ENV = os.environ.get('CRUMB_ENV')
    DEBUG = True
    POSTGRES_NAME = 'crumb_dev'
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = '5432'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASS = 'postgres'
    GRAPHIQL = True
    JWT_SECRET = 'super secret random key'
    SEND_SMS = False
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    CRUMB_IMAGES_BUCKET_NAME = 'crumb-image-uploads-dev'


class TestConfig(Config):
    TESTING = True
    POSTGRES_NAME = 'crumb_test'
    POSTGRES_PORT = '5433'
    GRAPHIQL = False
    # never set this to True! we don't want our
    # test suite sending texts to random people
    SEND_SMS = False


class ProdConfig(Config):
    DEBUG = False
    POSTGRES_NAME = os.environ.get('POSTGRES_NAME')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASS = os.environ.get('POSTGRES_PASS')
    GRAPHIQL = False
    JWT_SECRET = os.environ.get('JWT_SECRET')
    SEND_SMS = True
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_MOBILE_CLIENT = os.environ.get('AWS_SECRET_ACCESS_KEY')
    IMAGE_UPLOADS_BUCKET_NAME = 'crumb-image-uploads-prod'


def get_config_for_env():
    configs = {
        'dev': Config,
        'test': TestConfig,
        'prod': ProdConfig,
    }
    env = os.environ.get('CRUMB_ENV') or 'dev'

    return configs[env]


config_for_env = get_config_for_env()()
