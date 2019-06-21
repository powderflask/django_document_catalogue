django-document-cagtalogue Demo Project
=======================================

This folder contains a demo Django project that
illustrates a simple django-document-catalogue installation
with common settings and usage examples.

In particular, this project is intended / suited for develpment and interactive testing.
It is *NOT* production ready!

Running the demo
----------------

Install Dependencies:
    - python 3.x, django 2.x
    - django-document-catalogue + its dependencies

Run migrate, createsuperuser, and loaddata to configure DB::

    > manage.py migrate document_catalogue
    > manage.py createsuperuser
    > manage.py loaddata categories.json documents.json

Run django's test server, using the demo project settings::

    > python3 django_document_catalogue/demo/manage.py runserver 127.0.0.1:8001

Navigate to documents URL on your local host: http://127.0.0.1:8001/documents/

Browse to the various views provided by the demo.

 - You will need to create a user account with applicable permissions to upload documents.
 - A 'staff' user can create new categories via the django admin.

*Note on Fixtures*

Several data fixtures are included with the demo so it is "up-and-running"
with some categories and documents pre-loaded.

The folder:

    demo/media/documents

is populated with the document files for the data fixtures.
Modifying or deleting these media items will break the demo fixtures.
