# django-document-catalogue Demo Project

This folder contains a demo Django project to
illustrate a simple django-document-catalogue installation
with common settings and usage examples.

In particular, this project is intended / suited for development and interactive testing.
It is not intended to be production ready!


## Running the demo

Install Dependencies (see requirements.txt):
* python 3.x, django 2.x
* django-document-catalogue + its dependencies

Run migrate, createsuperuser, and loaddata to configure DB:

```console
> manage.py migrate
> manage.py createsuperuser
> manage.py loaddata categories.json documents.json
> manage.py collectstatic                            # not needed for dev. settings with DEBUG=True
```

Copy fixture media to private-media root (as defined in demo/settings):

```console
> cp -r fixtures/media ../private-media
```

Run django's test server, using the demo project settings:

```console
> manage.py runserver 127.0.0.1:8001
```

Navigate to the documents URL on your local host: http://127.0.0.1:8001/documents/

* Browse to the various views provided by the demo.
* Login as any 'staff' user to create new categories via the django admin.

#### *Note on Fixtures*

Several data fixtures are included with the demo so it is "up-and-running"
with some categories and documents pre-loaded.

These fixtures are located in `demo/fixtures/media/documents`.

The folder is populated with the document files for the data fixtures, and must be moved to the location set in 
settings.PRIVATE_STORAGE_ROOT (the default path is your-project-root/private-media). Failing to copy this media or 
modifying or deleting these media items will break the demo fixtures.
