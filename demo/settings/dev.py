"""
    This file configures the a local development environment to use the STAGE DB
"""
from .defaults import *
# no emails during local dev
ADMINS = ()
MANAGERS = ADMINS


# the django dev server so we will need to serve the static files (see urls.py)
DEBUG = True

INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}
