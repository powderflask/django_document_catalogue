from collections import namedtuple
from django.apps import AppConfig
import django.conf

def Map(type_name, **kwargs):
    # Returns a simple map of kwargs object
    mapType = namedtuple(type_name, kwargs.keys(),)
    return mapType(**kwargs)

class BaseCatalogueConfig(AppConfig):
    name = 'document_catalogue'
    verbose_name = 'Document Catalogue'

    # Default settings for the document_catalogue app.
    settings = Map(
        'default_settings',
        # Fine scale permissions (default permissions use DOCUMENT_CATALOGUE_LOGIN_REQUIRED, but that setting may be disabled by custom permissions)
        # Value is a dotted path to a permissions module or object with the required permissions functions - see permissions.py
        PERMISSIONS = getattr(django.conf.settings,
                              'DOCUMENT_CATALOGUE_PERMISSIONS', 'document_catalogue.permissions'),

        # Enable document editing URL's and the Ajax document API
        # When disabled, documents are managed via the django.admin
        # When enabled, be sure to carefully consider the permissions on these views!
        ENABLE_EDIT_URLS = getattr(django.conf.settings,
                                   'DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS', False),

        # Root directory for file uploads to the document catalogue
        # If private-files is used, media_root will be a sub-directory of PRIVATE_STORAGE_ROOT
        MEDIA_ROOT = getattr(django.conf.settings,
                             'DOCUMENT_CATALOGUE_MEDIA_ROOT', 'documents/'),

        # Upload file settings - constrain the file content_types and max. filesize for document file uploads.
        # None to allow any file type - eliminates dependency on python-magic and libmagic, which are included only if a whitelist is supplied.
        #   e.g.  DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST = ('application/pdf', 'image/png', 'image/jpg')
        CONTENT_TYPE_WHITELIST = getattr(django.conf.settings,
                                         'DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST', None),
        # max. size in bytes, None for no limit
        MAX_FILESIZE = getattr(django.conf.settings,
                               'DOCUMENT_CATALOGUE_MAX_FILESIZE', 10 * 1024 * 1024),

        # Plugin Classes used to inject behaviours into standard document list views
        # Define plugins by extending the ABC: document_catalogue.plugins.AbstractViewPlugin
        # Inject them by customizing this setting
        LIST_VIEW_PLUGINS = getattr(django.conf.settings,
                                    'DOCUMENT_CATALOGUE_LIST_VIEW_PLUGINS',
                                    ('document_catalogue.plugins.SessionOrderedViewPlugin',)),
   )


class PrivateCatalogueConfig(BaseCatalogueConfig):
    verbose_name = 'Private Catalogue'

    USE_PRIVATE_FILES = True
    LOGIN_REQUIRED_DEFAULT = True

    settings = Map(
        "private_settings",
        USE_PRIVATE_FILES = True,
        LOGIN_REQUIRED = getattr(django.conf.settings,
                                 'DOCUMENT_CATALOGUE_LOGIN_REQUIRED', True),
        **BaseCatalogueConfig.settings._asdict()
    )



class PublicCatalogueConfig(BaseCatalogueConfig):
    verbose_name = 'Public Catalogue'

    USE_PRIVATE_FILES = False
    LOGIN_REQUIRED_DEFAULT = False
    settings = Map(
        "public_settings",
        USE_PRIVATE_FILES=False,
        # IMPORTANT: this only restricts access to the Catalogue views - anyone with a file's URL can download it!
        LOGIN_REQUIRED = getattr(django.conf.settings,
                                 'DOCUMENT_CATALOGUE_LOGIN_REQUIRED', False),
        **BaseCatalogueConfig.settings._asdict()
    )
