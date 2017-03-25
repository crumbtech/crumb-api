import os

POSTGRES_HOST = os.environ.get('POSTGRES_HOST') or 'localhost'
POSTGRES_PORT = os.environ.get('POSTGRES_PORT') or '5432'
POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'postgres'
POSTGRES_PASS = os.environ.get('POSTGRES_PASS') or 'postgres'

POSTGRES = {
    'drivername': 'postgres',
    'host': POSTGRES_HOST,
    'port': POSTGRES_PORT,
    'username': POSTGRES_USER,
    'password': POSTGRES_PASS,
}
