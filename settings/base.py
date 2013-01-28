import os

SRC_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(SRC_ROOT, 'static')
STATIC_URL = '/static/'

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
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cousinade.urls'
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (os.path.join(SRC_ROOT, 'templates'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'compressor',
    'django_tables2',
    'cousinade',
)
