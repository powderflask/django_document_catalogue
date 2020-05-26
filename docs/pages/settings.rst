.. _settings:

Settings
========

Default app settings values can be overridden in the normal way...

.. _settings-file-storage:

File Storage
############

Media Root
^^^^^^^^^^
Root directory for file uploads to the document catalogue::

    DOCUMENT_CATALOGUE_MEDIA_ROOT = 'documents/'

PrivateCatalogueConfig
----------------------
* directory will be a sub-directory of :code:`PRIVATE_STORAGE_ROOT`

PublicCatalogueConfig
---------------------
* directory will be sub-directory of :code:`MEDIA_ROOT`

Upload Restrictions
^^^^^^^^^^^^^^^^^^^
Constrain document file uploads by file content_type and file size::

    DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST = None      # allow any file type
    DOCUMENT_CATALOGUE_MAX_FILESIZE = 10 * 1024 * 1024    # 10 Mb

* Whitelist is a sequence of content_types.  E.g, :code:`('application/pdf', 'image/png', 'image/jpg')`
    * If supplied, all other content types will fail to validate on upload.
    * for :code:`PublicCatalogueConfig`, whitelist creates dependency on :code:`python-magic`,
       which is imported only if a whitelist is supplied
* Max. file size is in bytes, use None for no limit on upload filesize (not recommended - subject to DOS attack and server timeouts)

.. _settings-access-control:

Access Control
##############

Login Required
^^^^^^^^^^^^^^
Restrict catalogue access to logged in users only::

    DOCUMENT_CATALOGUE_LOGIN_REQUIRED = True  # if PrivateCatalogueConfig else False

**IMPORTANT**: *setting restricts access to catalogue views only -- not to media served directly by web server.*
For :code:`PublicCatalogueConfig`, anyone with the correct media URL can download files directly
regarless of this setting.

Enable Edit Views
^^^^^^^^^^^^^^^^^
Enable document editing URL's and the Ajax document API for user-facing edit views::

    DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS = False

* When disabled, documents are managed via the :code:`django.admin`
* When enabled, be sure to carefully consider the permissions for these views!

Plugin Permissions
^^^^^^^^^^^^^^^^^^
Swap in your own permissions module::

    DOCUMENT_CATALOGUE_PERMISSIONS = 'document_catalogue.permissions'

* Value is a dotted path to a permissions module or object with the required permissions functions

See :ref:`plugin-permissions`

PrivateCatalogueConfig
----------------------
Swap in your own file access control function::

    PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_superuser'

* See `private-storage Access Rules <https://github.com/edoburu/django-private-storage#defining-access-rules>`_

.. _settings-plugins:

Inject Behaviours
#################

Document List View Plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^
Plugin Classes used to inject behaviours into standard document list views::

    DOCUMENT_CATALOGUE_LIST_VIEW_PLUGINS = ('document_catalogue.plugins.SessionOrderedViewPlugin', )

* Value is a dotted path to a plugin class that extends :code:`document_catalogue.plugins.AbstractViewPlugin`

See :ref:`doc-list-plugins`
