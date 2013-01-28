import os

SRC_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ADMINS = (
    ('You', 'you@there'),
)

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr-fr'
USE_L10N = True

STATIC_ROOT = os.path.join(SRC_ROOT, 'static')
STATIC_URL = '/static/'
# static for our static files, media for user-uploaded pictures
MEDIA_ROOT = os.path.join(SRC_ROOT, 'media')
MEDIA_URL = '/media/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = 'rezk$80u7u1+n+61arn5))z%8&amp;vhg@^sg71j!o+a4evjq*e6!7'

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cousinade.auth.AuthenticationMiddleware',
)

ROOT_URLCONF = 'cousinade.urls'
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (os.path.join(SRC_ROOT, 'templates'),)
FIXTURE_DIRS = (os.path.join(SRC_ROOT, 'fixtures'),)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.tz',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'compressor',
    'django_tables2',
    'cousinade',
)

LOGIN_URL = '/login'
LOGIN_EXEMPT_URLS = ['password/request', 'password/do', 'static/']
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SESSION_EXPIRE = 60*20

EMAIL_SUBJECT_PREFIX = '[Cousinade admin] '
