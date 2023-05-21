Setup
=====

Installation
^^^^^^^^^^^^

Install from PyPI with ``pip``::

    pip install django-document-catalogue


Configuration
^^^^^^^^^^^^^

PrivateStorageConfig
--------------------
This config allows you to restrict or control access to file downloads...

Add app and dependencies to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'document_catalogue.apps.PrivateCatalogueConfig',
        'mptt',
        'private_storage',
        ...
    )

Add paths to ``urls.py``::

    urlpatterns += [
        path('documents/', include('document_catalogue.urls')),
        path('private-media/', include('private_storage.urls')),
    ]

Configure ``django-private-storage``
####################################

* :code:`pip install django-private-storage`
* `configure private-storage <https://github.com/edoburu/django-private-storage#configuration>`_, pay special attention to::

    PRIVATE_STORAGE_ROOT = '/path/to/private-media/'     # this path should be outside your web server root!
    PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_authenticated'


PublicStorageConfig
--------------------
If none of your files require login or permissions to download...

Add app to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'document_catalogue.apps.PublicCatalogueConfig',
        ...
    )

Add paths to ``urls.py``::

    urlpatterns += [
        path('documents/', include('document_catalogue.urls')),
    ]

Additional Dependencies
#######################
* :code:`pip install django-constrainedfilefield` `<https://github.com/mbourqui/django-constrainedfilefield#installation>`_
    * you may need to build `libmagic <https://github.com/ahupp/python-magic#installation>`_  E.g., ::

        brew install libmagic

Migrate
-------
Migrate models::

    python manage.py migrate


Options
-------

Document Ordering
#################

Documents have `sort_order` field that plays nicely with `django-admin-sortable2 <https://django-admin-sortable2.readthedocs.io>`_
For drag-and-drop re-ordering in django Admin, simply::

    pip install django-admin-sortable2

