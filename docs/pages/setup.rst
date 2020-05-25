Setup
=====

Installation
^^^^^^^^^^^^

Install from PyPI with ``pip``::

    pip install django-document-catalogue


Configuration
^^^^^^^^^^^^^

Add app and dependencies to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'document_catalogue',
        'mptt',
        'private_storage',    # or opt-out: settings.DOCUMENT_CATALOGUE_USE_PRIVATE_FILES = False
        ...
    )

Add paths to ``urls.py``::

    urlpatterns += [
        path('documents/', include('document_catalogue.urls')),
        path('private-media/', include('private_storage.urls')),   # or opt-out: settings.DOCUMENT_CATALOGUE_USE_PRIVATE_FILES = False
    ]

Migrate models::

    python manage.py migrate


Options
-------

Document Ordering
#################

Documents have `sort_order` field that plays nicely with `django-admin-sortable2 <https://django-admin-sortable2.readthedocs.io>`_
For drag-and-drop re-ordering in django Admin, simply::

    pip install django-admin-sortable2


Public Files
############

Opt-out of `private-files` and use a `constrained-file` field instead.
In `settings.py`::

    DOCUMENT_CATALOGUE_USE_PRIVATE_FILES = False

You may need to build `libmagic <https://github.com/ahupp/python-magic#installation>`_ ::

    brew install libmagic
