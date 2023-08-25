Quick Start Guide
=================


Quick start
-----------

* :code:`pip install -r requirements.txt`
* :code:`python3 setup.py test`   (to run app test suite)

1. Add apps to your INSTALLED_APPS settings::

    INSTALLED_APPS = [
        ...
        'document_catalogue',
        'mptt',
        'private_storage',
    ]

2. Configure settings:

* override document catalogue default settings (if required)
* private storage settings (if using)

3. Include the document_catalogue URLconf (and optionally private_storage)::

    path('documents/', include('document_catalogue.urls')),
    path('private-media/', include('private_storage.urls')),

4. Run :code:`python manage.py migrate` to create the document_catalogue models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create some Categories and Documents (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/documents/ to browse your catalogue by category.


Next Steps
----------

See the demo project for some ideas on how to configure and use the Document Catalogue.

 * add document_catalogue/base.html to your templates to override the base template.
   Document Catalogue views are rendered within :code:`{% block dc-content %}`
 * add a :code:`<div id='DocumentCatalogueManager' ...>` to base template to enable dropzone uploads and provide default options
 * see demo project for more ideas


