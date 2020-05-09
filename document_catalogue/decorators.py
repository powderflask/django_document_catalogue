from importlib import import_module
from django.core.exceptions import PermissionDenied
from . import settings

permissions = import_module(settings.DOCUMENT_CATALOGUE_PERMISSIONS)


def permission_required(permission_fn):
    """
        Constructs a CBV decorator that checks permission_fn(view.request.user, view.kwargs) before calling
          view.dispatch to test if request.user has a given (object) permission.
        Usage:  @permission_required("permission_function_name")  class MyViewClass: ...
    """
    def decorator(view_class):
        _dispatch = view_class.dispatch

        def dispatch(self, request, *args, **kwargs):
            if not permission_fn(request.user, **self.kwargs):
                raise PermissionDenied()
            return _dispatch(self, request, *args, **kwargs)

        view_class.dispatch = dispatch
        return view_class

    return decorator
