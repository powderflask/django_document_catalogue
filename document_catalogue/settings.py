"""Default settings for the document_catalogue app."""

from django.conf import settings
from django.apps import apps

appConfig = apps.get_app_config('document_catalogue')

# To use django-private-storage as storage backend for supporting documentation files
# If True, pip install django-private-storage and configure settings for private file storage as per docs
# Intended to be set at start of project and not changed - schema and data migration required if this changes!
DOCUMENT_CATALOGUE_USE_PRIVATE_FILES = appConfig.USE_PRIVATE_FILES

# IMPORTANT: this only restricts access to the Catalogue views - if private-files is not used, anyone with thier URL can download them!
DOCUMENT_CATALOGUE_LOGIN_REQUIRED = getattr(settings, 'DOCUMENT_CATALOGUE_LOGIN_REQUIRED', appConfig.LOGIN_REQUIRED_DEFAULT)

# Fine scale permissions (default permissions use DOCUMENT_CATALOGUE_LOGIN_REQUIRED, but that setting may be disabled by custom permissions)
# Value is a dotted path to a permissions module or object with the required permissions functions - see permissions.py
DOCUMENT_CATALOGUE_PERMISSIONS = getattr(settings, 'DOCUMENT_CATALOGUE_PERMISSIONS', 'document_catalogue.permissions')

# Enable document editing URL's and the Ajax document API
# When disabled, documents are managed via the django.admin
# When enabled, be sure to carefully consider the permissions on these views!
DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS = getattr(settings, 'DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS', False)

# Root directory for file uploads to the document catalogue
# If private-files is used, media_root will be a sub-directory of PRIVATE_STORAGE_ROOT
DOCUMENT_CATALOGUE_MEDIA_ROOT = getattr(settings, 'DOCUMENT_CATALOGUE_MEDIA_ROOT', 'documents/')

# Upload file settings - constrain the file content_types and max. filesize for document file uploads.
# None to allow any file type - eliminates dependency on python-magic and libmagic, which are included only if a whitelist is supplied.
#   e.g.  DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST = ('application/pdf', 'image/png', 'image/jpg')
DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST = getattr(settings,'DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST', None)
# max. size in bytes, None for no limit
DOCUMENT_CATALOGUE_MAX_FILESIZE = getattr(settings, 'DOCUMENT_CATALOGUE_MAX_FILESIZE', 10 * 1024 * 1024)

# Plugin Classes used to inject behaviours into standard document list views
# Define plugins by extending the ABC: document_catalogue.plugins.AbstractViewPlugin
# Inject them by customizing this setting
DOCUMENT_CATALOGUE_LIST_VIEW_PLUGINS = getattr(settings, 'DOCUMENT_CATALOGUE_LIST_VIEW_PLUGINS',
                                               ('document_catalogue.plugins.SessionOrderedViewPlugin', ))