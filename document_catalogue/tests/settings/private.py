""" Settings for PrivateCatalogueConfig tests """
from .base import *

INSTALLED_APPS += [
    'document_catalogue.apps.PrivateCatalogueConfig',
    'private_storage',
]

# django-private-files  (private document downloads)
PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, "private-media/")
PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_authenticated'
