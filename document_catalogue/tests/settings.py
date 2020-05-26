"""
Django settings for testing document_catalogue.
"""

from pathlib import Path
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = '/tmp/document_catalogue_tests/'

# Ensure the base path exists
Path(BASE_DIR).mkdir(parents=True, exist_ok=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'foobar'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'document_catalogue.apps.PrivateCatalogueConfig',
    'mptt',
    'private_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'document_catalogue.tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'demo/templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Media files (document uploads)
# https://docs.djangoproject.com/en/2.2/howto/static-files/#serving-uploaded-files-in-development

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static/"),
    # '/path/to/some_other_static_media',
)

# django-private-files  (private document downloads)
PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, "private-media/")
PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_authenticated'

# Document Catalogue overrides
DOCUMENT_CATALOGUE_LOGIN_REQUIRED = True
DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS = True
DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST = ('text/plain', )
DOCUMENT_CATALOGUE_MAX_FILESIZE = 1 * 1024 * 1024

