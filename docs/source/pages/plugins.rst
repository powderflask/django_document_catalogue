Swappable Behaviours
====================

.. _plugin-permissions:

Plugin Permissions
^^^^^^^^^^^^^^^^^^

Catalogue Access Control / Permissions are determined by a Python module, that can be swapped out using a setting::

    DOCUMENT_CATALOGUE_PERMISSIONS = 'document_catalogue.permissions'   # default

Override by providing an ordinary Python module that defines the permission functions.
See :ref:`Permissions API <api-permissions>`

By default, these functions simply use django's built-in permissions model::

    document_catalogue.change_document
    document_catalogue.add_document
    document_catalogue.delete_document

To simply restrict access to logged in users only, use setting::

    DOCUMENT_CATALOGUE_LOGIN_REQUIRED = True    # default

See :ref:`Access Control Settings <settings-access-control>`

PrivateCatalogueConfig
----------------------
Document download permissions are determined by a Python function::

    PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_superuser'

* See `private-storage Access Rules <https://github.com/edoburu/django-private-storage#defining-access-rules>`_


.. _doc-list-plugins:

Document List View Plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^

Inject custom behaviours into views that list documents using a simple plugin registered on the view.

Plugin API
----------

Extend the Abstract Base Class and override method(s) to customize behaviours

See :ref:`Plugins API <api-plugins>`


Inject your plugin(s) behaviours into document list views using a setting::

    DOCUMENT_CATALOGUE_LIST_VIEW_PLUGINS = ('document_catalogue.plugins.SessionOrderedViewPlugin', )  # default

See :ref:`Plugin Settings <settings-plugins>`

Batteries Included
##################

Document Catalogue comes with 2 plugins:

.. py:currentmodule:: document_catalogue.plugins
.. autoclass:: OrderedViewPlugin
   :noindex:

.. autoclass:: SessionOrderedViewPlugin
   :noindex:
