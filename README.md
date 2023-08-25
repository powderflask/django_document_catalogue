# Django Document Catalogue
#### Version: 0.4.0

[![Tests](https://github.com/JacobTumak/django_document_catalogue/actions/workflows/pytest.yaml/badge.svg)](https://github.com/JacobTumak/django_document_catalogue/actions/workflows/pytest.yaml)

Simple, light-weight, stand-alone, hierarchical document library as a
reusable django app.

## Use Case:
 * you need a library of static media documents (PDF or other formats);
 * documents are organized in hierarchical categories;

## Features:
 * permanent URLs for direct access to document, category, and file download (even if filename changes)
 * opt-out private file storage (file storage / downloads protected by login, on by default)
 * plugin permissions settings
 * plugin document list view customization
 * upload / edit / delete documents via django admin, and/or..,
 * opt-in user-facing edit / upload / delete views and AJAX API

## Dependencies:
 * python 3.7+
 * django 3.2+
 * [django-mptt](https://django-mptt.readthedocs.io/en/latest/index.html)

### Configurable file handling:
 * [django-private-storage](https://pypi.org/project/django-private-storage/)

 or

 * [django-constrainedfilefield](https://github.com/mbourqui/django-constrainedfilefield)
 * [python-magic](https://github.com/ahupp/python-magic) (if you want to validate file content_types)

### Opt-in:
 * [dropzone](https://www.dropzonejs.com/): drag-and-drop file uploads
 * [django-admin-sortable2](https://django-admin-sortable2.readthedocs.io): drag-and-drop document ordering

## Get Me Some of That
* [Source Code](https://github.com/powderflask/django_document_catalogue)
* [Read The Docs](https://django-document-catalogue.readthedocs.io/en/latest/)
* [Issues](https://github.com/powderflask/django_document_catalogue/issues)
* [PyPI](https://pypi.org/project/django-document-catalogue)

[MIT License](https://github.com/powderflask/django_document_catalogue/blob/master/LICENSE)