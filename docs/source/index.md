# Django Document Catalogue

Simple, light-weight, stand-alone, hierarchical document library as a
reusable django app.

## Use Case
 * you need a library of static media documents (PDF or other formats);
 * documents are organized in hierarchical categories;

## Features
 * permanent URLs for direct access to document, category, and file download (even if filename changes when document is updated)
 * opt-out [private file storage](https://github.com/edoburu/django-private-storage#django-private-storage)
   (file storage / downloads protected by login, on by default)
 * upload / edit / delete documents via django admin, and/or...
 * opt-in user-facing edit / upload / delete views and AJAX API  (off by default)
 * plug-in permissions settings
 * plug-in document list view customization (ordering menu on by default)
 * plays nice with [dropzone](https://www.dropzonejs.com/) for drag-and-drop file uploads
 * plays nice with [django-admin-sortable2](https://django-admin-sortable2.readthedocs.io) for drag-and-drop document ordering in admin

```{toctree}
:maxdepth: 2
:caption: Getting Started

pages/setup
pages/quick_start
```

```{toctree}
:maxdepth: 2
:caption: Customization

pages/settings
pages/plugins
```

```{toctree}
:maxdepth: 2
:caption: Reference

api/index
genindex
search
```