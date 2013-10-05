from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'local.db',                      # Or path to database file if using sqlite3.
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

BASE_URL = '127.0.0.1:8000'

PASSWORD_RESET_FROM = 'no-reply@you'
SITE_NAME = 'cousinade You'
