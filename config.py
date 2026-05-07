import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    DEBUG = os.environ.get('DEBUG') or True
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'MySQL:///healthy_mate.db'
    JSONIFY_PRETTYPRINT_REGULAR = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE') or False
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True