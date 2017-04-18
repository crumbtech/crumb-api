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


class TestConfig(Config):
    TESTING = True
    POSTGRES_NAME = 'crumb_test'
    POSTGRES_PORT = '5433'
    GRAPHIQL = False


class ProdConfig(Config):
    DEBUG = False
    POSTGRES_NAME = os.environ.get('POSTGRES_NAME')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASS = os.environ.get('POSTGRES_PASS')
    GRAPHIQL = False
    JWT_SECRET = os.environ.get('JWT_SECRET')


def get_config_for_env():
    configs = {
        'dev': Config,
        'test': TestConfig,
        'prod': ProdConfig,
    }
    env = os.environ.get('CRUMB_ENV') or 'dev'

    return configs[env]


for_env = get_config_for_env()()
