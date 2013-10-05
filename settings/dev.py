from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SRC_ROOT, 'local.db'),
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
