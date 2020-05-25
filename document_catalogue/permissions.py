"""
Functions used to control access to views (Permission Denied returned when false)
    and to enable/disable interactions in the templates.

Default permissions module can be swapped out in settings.
Defaults use django's built in content_type permissions for the Document model.

Each function takes the request use and the view's kwargs as arguments,
    returns True iff user has the required permission for the given object(s).
"""
from . import settings


def user_can_view_document_catalogue(user, **kwargs):
    """ Return True iff given user is allowed to view the document catalogue """
    return not settings.DOCUMENT_CATALOGUE_LOGIN_REQUIRED or user.is_authenticated


def user_can_download_document(user, **kwargs):
    """ Return True iff the given user is allowed to download documents"""
    return user_can_view_document_catalogue(user, **kwargs)


def user_can_edit_document(user, **kwargs):
    """ Return True iff the given user can edit documents in the catalogue """
    return user.is_staff or user.has_perm('document_catalogue.change_document')


def user_can_post_document(user, **kwargs):
    """ Return True iff the given user can upload new files to the catalouge """
    return user.is_staff or user.has_perm('document_catalogue.add_document')


def user_can_delete_document(user, **kwargs):
    """ Return True iff the given user can delete documents from the catalogue """
    return user.is_staff or user.has_perm('document_catalogue.delete_document')
