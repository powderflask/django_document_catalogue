"""Default settings for the document_catalogue app."""

from django.conf import settings


# IMPORTANT: this only prevents access to the Catalogue views - the documents are served as media, anyone with thier URL can download them!
DOCUMENT_CATALOGUE_LOGIN_REQUIRED = getattr(settings, 'DOCUMENT_CATALOGUE_LOGIN_REQUIRED', True)

# Fine scale permissions (default permissions use DOCUMENT_CATALOGUE_LOGIN_REQUIRED, but that setting may be disabled by custom permissions)
# Value is a dotted path to a permissions module or object with the required permisisons functions - see permissions.py
DOCUMENT_CATALOGUE_PERMISSIONS = getattr(settings, 'DOCUMENT_CATALOGUE_PERMISSIONS', 'document_catalogue.permissions')

# Enable document editing URL's and the Ajax document API
# When disabled, documents are managed via the django.admin
# When enabled, be sure to carefully consider the permissions on these views!
DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS = getattr(settings, 'DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS', False)

# Root directory for file uploads to the document catalogue
DOCUMENT_CATALOGUE_MEDIA_ROOT = getattr(settings, 'DOCUMENT_CATALOGUE_MEDIA_ROOT', settings.MEDIA_ROOT+'documents')

# Upload file settings - constrain the file content_types and max. filesize for document file uploads.
# None to allow any file type - eliminates dependency on python-magic and libmagic, which are included only if a whitelist is supplied.
#   e.g.  DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST = ('application/pdf', 'image/png', 'image/jpg')
DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST = getattr(settings,'DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST', None)
# max. size in Mb, None or 0 for no limit
DOCUMENT_CATALOGUE_MAX_FILESIZE = getattr(settings, 'DOCUMENT_CATALOGUE_MAX_FILESIZE', 10)