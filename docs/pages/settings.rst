.. _settings:

Settings
========

Default app settings values can be overridden in the normal way...

.. _settings-file-storage:

File Storage
############

Private Files
^^^^^^^^^^^^^
Store files outside web root and serve them via django so permissions can be applied to downloads,
use django-private-storage as storage backend for storing files::

    DOCUMENT_CATALOGUE_USE_PRIVATE_FILES = True

* If True, :code:`pip install django-private-storage` and `configure private-storage <https://github.com/edoburu/django-private-storage#configuration>`_
* If False, :code:`pip install django-constrainedfilefield` `<https://pypi.org/project/django-constrainedfilefield/>`_

**IMPORTANT**: *Intended to be set at start of project and not changed - schema and data migration required if this changes!*

Media Root
^^^^^^^^^^
Root directory for file uploads to the document catalogue::

    DOCUMENT_CATALOGUE_MEDIA_ROOT = 'documents/'

* If :code:`private-files` is used, this directory will be a sub-directory of :code:`PRIVATE_STORAGE_ROOT`
* Otherwise, it will be a sub-directory under django's normal :code:`MEDIA_ROOT`

Upload Restrictions
^^^^^^^^^^^^^^^^^^^
Constrain document file uploads by file content_type and file size::

    DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST = None      # allow any file type
    DOCUMENT_CATALOGUE_MAX_FILESIZE = 10 * 1024 * 1024    # 10 Mb

* Whitelist is a sequence of content_types.  E.g, :code:`('application/pdf', 'image/png', 'image/jpg')`
    * If supplied, all other content types will fail to validate on upload.
    * Whitelist creates dependency on :code:`python-magic`, which is imported only if a whitelist is supplied (if not using :code:`private-files`)
* Max. file size is in bytes, use None for no limit on upload filesize (not recommended - subject to DOS attack and server timeouts)

.. _settings-access-control:

Access Control
##############

Login Required
^^^^^^^^^^^^^^
Restrict access to catalogue to logged in users only::

    DOCUMENT_CATALOGUE_LOGIN_REQUIRED = True

**IMPORTANT**: *setting restricts access to catalogue views only -- not to media served directly by web server.*
If :code:`private-files` not used, anyone with the correct media URL can download files directly
regarless of this setting.

Enable Edit Views
^^^^^^^^^^^^^^^^^
Enable document editing URL's and the Ajax document API for user-facing edit views::

    DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS = False

* When disabled, documents are managed via the django.admin
* When enabled, be sure to carefully consider the permissions for these views!

Plugin Permissions
^^^^^^^^^^^^^^^^^^
Swap in your own permissions module::

    DOCUMENT_CATALOGUE_PERMISSIONS = 'document_catalogue.permissions'

* Value is a dotted path to a permissions module or object with the required permissions functions

See :ref:`plugin-permissions`

.. _settings-plugins:

Inject Behaviours
#################

Document List View Plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^
Plugin Classes used to inject behaviours into standard document list views::

    DOCUMENT_CATALOGUE_LIST_VIEW_PLUGINS = ('document_catalogue.plugins.SessionOrderedViewPlugin', )

* Value is a dotted path to a plugin class that extends :code:`document_catalogue.plugins.AbstractViewPlugin`

See :ref:`doc-list-plugins`
