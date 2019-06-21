"""
     Base classes used to setup testing fixtures
"""
from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User, Permission
from django.utils.text import slugify
from document_catalogue import models


def create_user(username='myUser', permissions=()):
    """
        Factory function to create and return a single user with the given iterable of permissions.
        Common DC permissions:  ('Can add document', 'Can change document', 'Can delete document')
    """
    user = User.objects.create_user(
        first_name=username.capitalize(), last_name="Lastname", email="{username}@example.com".format(username=username),
        username=username, password="password",
    )
    if permissions:
        permissions = Permission.objects.filter(name__in=permissions)
        user.user_permissions.set(permissions)

    print("Created user", user)
    return user


def create_document_categories(category_names=(('Top Level Category 1', (('Sub-Category 1A', ()), ('Sub-Category 1B', ()), )),
                                               ('Top Level Category 2', (('Sub-Category 2A', ()), ))
                                              ),
                               parent=None,
                               description_template='This is the description for {slug}',
                               ):
    """
        Factory function to create and return a list of DocumentCategory objects.
        Hierarchy defined by nesting of 2-tuples in category_names.
    """
    def create_category(name, parent=None):
        slug = slugify(name)
        return models.DocumentCategory.objects.create(name=name, slug=slug, parent=parent,
                                                      description=description_template.format(slug=slug))

    categories = []
    for name, children in category_names:
        cat = create_category(name, parent=parent)
        categories += [cat] + create_document_categories(children, parent=cat)

    return categories


def generate_file(filename, file_type='txt'):
    def write_text_file(filename, content):
        with open(filename, 'wb') as myfile :
            myfile.write(content)
            return myfile

    if file_type is 'txt':
        return write_text_file(filename, b'Hello World')

    if file_type is 'html':
        return write_text_file(filename, b'<!DOCTYPE html><html><head></head><body><p>Hello World</p></body></html>')

    raise Exception("Don't know how to generate file of type %s"%file_type)
