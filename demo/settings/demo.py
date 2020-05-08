"""
    This file configures a demo environment
"""
from demo.settings.defaults import *
# no emails during local dev
ADMINS = ()
MANAGERS = ADMINS


# the django dev server so we will need to serve the static files (see urls.py)
DEBUG = True

INTERNAL_IPS = ['207.34.177.126', ]  # List of developer's IP's who need to debug on production server

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
#   see: https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/#secret-key
with open('/home/driftwoodcove/secrets/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# django security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# check --deploy recommended, but not sure value is added; careful testing required.
# SECURE_HSTS_SECONDS = 3600  # enables HTTP Strict Transport Security; careful testing required.  see: https://docs.djangoproject.com/en/1.11/ref/middleware/#http-strict-transport-security
# SECURE_CONTENT_TYPE_NOSNIFF = True # seems not required;  rcareful testing required - project and report attachments
# X_FRAME_OPTIONS = 'DENY'  # but fileDownload uses an iframe for file downloads - careful testing required.

ALLOWED_HOSTS = ['docs.driftwoodcove.ca', '207.38.94.41']

STATIC_ROOT = '/home/driftwoodcove/webapps/django_doccat_static'