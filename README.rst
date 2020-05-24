
Document Catalogue
==================

Simple, light-weight, stand-alone, hierarchical document library as a
reusable django app.

Use Case:
 * you need a library of static media documents (PDF or other formats);
 * documents are organized in hierarchical categories;

Features:
 * permanent URLs for direct access to document, category, and file download (even if filename changes)
 * opt-out private files (file downloads protected by login, on by default)
 * plugin permissions settings
 * plugin document list view customization (list ordering menu on by default)
 * upload / edit / delete documents via django admin, and/or..,
 * opt-in user-facing edit / upload / delete views and AJAX API  (off by default)
 * plays nice with `dropzone <https://www.dropzonejs.com/>`_ for drag-and-drop file uploads
 * plays nice with `django-admin-sortable2 <https://django-admin-sortable2.readthedocs.io>`_ for drag-and-drop document ordering in admin

Dependencies:
 * python 3
 * django 2
 * `django-mptt <https://django-mptt.readthedocs.io/en/latest/index.html>`_

Opt-in:
 * `django-private-storage <https://pypi.org/project/django-private-storage/>`_

 or

 * `django-constrainedfilefield <https://github.com/mbourqui/django-constrainedfilefield>`_
 * `python-magic <https://github.com/ahupp/python-magic>`_ (if you want to validate file content_types)

< Detailed documentation > (TODO)


Quick start
-----------

* `pip install -r requirements.txt`
* `brew install libmagic` (for OSX using homebrew, see `python-magic docs <https://github.com/ahupp/python-magic#installation>`_ for more info.
* `python3 setup.py test`   (to run app test suite)

1. Add "document_catalogue" and "mptt"  (and optionally "private_storage") to your INSTALLED_APPS settings::

    INSTALLED_APPS = [
        ...
        'document_catalogue',
        'mptt',
        'private_storage',    # or opt-out: settings.DOCUMENT_CATALOGUE_USE_PRIVATE_FILES = False
    ]
    
2. Configure settings::

  * override document catalogue default settings (if required)
  * private storage settings (if using)

3. Include the document_catalogue URLconf (and optionally private_storage)::

    path('documents/', include('document_catalogue.urls')),
    path('private-media/', include('private_storage.urls')),   # or opt-out: settings.DOCUMENT_CATALOGUE_USE_PRIVATE_FILES = False

4. Run `python manage.py migrate` to create the document_catalogue models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create some Categories and Documents (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/documents/ to browse your catalogue by category.


Next Steps
----------

See the demo project for some ideas on how to configure and use the Document Catalogue.

 * add document_catalogue/base.html to your templates to override the base template.
   Document Catalogue views are rendered within `{% block dc-content %}`
 * add `scripts`: jquery, bootstrap, dropzone, and `static/document_catalogue/document_catalogue.js` to base template
 * add a `<div id='DocumentCatalogueManager' ...>` to base template to enable dropzone uploads and provide default options


License
-------

The code is available under the `MIT license <LICENSE.txt>`_.
