from __future__ import unicode_literals
from importlib import import_module

from django.apps import apps
from django import template

appConfig = apps.get_app_config('document_catalogue')

# import Plugin Permissions module
permissions = import_module(appConfig.settings.PERMISSIONS)

register = template.Library()

def has_permission(user, perm):
    check_perm = getattr(permissions, perm, lambda user: False)
    return check_perm(user) if callable(check_perm) else False

@register.filter(name='can')
def can_template_tag(user, permission):
    return has_permission(user, permission)
