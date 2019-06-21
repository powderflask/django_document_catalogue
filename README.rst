
Document Catalogue
==================

Simple, light-weight, stand-alone, hierarchical document library as a
reusable django app.

Use Case:
 * you need a library of static media documents (PDF or other formats);
 * documents are organized in hierarchical categories;

Features:
 * URLs for direct access to document, category, and file download
 *  < 'semi-private' file download URL's > (FUTURE)
 * plugin permissions settings
 * upload / edit / delete documents via django admin
    * optionally, enable user-facing edit / upload / delete views and AJAX API
    * plays nice with dropzone for simple file uploads

Dependencies:
 * python 3
 * django 2
 * [django-mptt](https://django-mptt.readthedocs.io/en/latest/index.html)
 * [django-constrainedfilefield] (https://github.com/mbourqui/django-constrainedfilefield)
 * python-magic (if you want to validate file content_types)

Detailed documentation is in the "docs" directory.


Quick start
-----------

`pip install -r requirements.txt`
'brew install libmagic`   (for OSX using homebrew, see [python-magic docs](https://github.com/ahupp/python-magic#installation) for more info.

1. Add "document_catalogue" and "mptt" to your INSTALLED_APPS setting like this::

    ```
    INSTALLED_APPS = [
        ...
        'document_catalogue.apps.DocumentCatalogueConfig',
        'mptt',
    ]
    ```
    
2. Include the document_catalogue URLconf in your project urls.py like this::
    ```
    path('documents/', include('document_catalogue.urls')),
    ```
3. Run `python manage.py migrate` to create the document_catalogue models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create some Categories and Documents (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/documents/ to browse your catalogue by category.


Next Steps
----------

See the demo project for some ideas on how to configure and use the Document Catalogue.

 * add document_catalogue/base.html to your templates to override the base template.
   Document Catalogue views are rendered within `{% block dc-content %}`
 * add `scripts`: jquery, dropzone, and `static/document_catalogue/document_catalogue.js` to base template
 * add a `<div id='DocumentCatalogueManager' ...>` to base template to enable dropzone uploads and provide default options


License
-------

The code is available under the [MIT license](LICENSE.txt).
