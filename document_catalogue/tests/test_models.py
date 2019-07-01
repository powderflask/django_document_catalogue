import os

from django.test import TestCase
from django import forms
from document_catalogue import models
from . import base

# Create tests for models here.

class CategoryTests(TestCase):
    """
        Test basic behaviours for DocumentCategory model
    """
    def setUp(self):
        super().setUp()
        self.categories=base.create_document_categories()

    def test_get_absolute_url(self):
        categories = models.DocumentCategory.objects.all()
        for cat in categories:
            self.assertIn(cat.slug, cat.get_absolute_url(), 'URL for category should contain its slug.')

    def test_has_children(self):
        categories = models.DocumentCategory.objects.filter(parent=None)
        for cat in categories:
            self.assertTrue(cat.has_children(), 'Category reporting no children when it has sub-categories.')

    def test_not_has_children(self):
        cat = models.DocumentCategory.objects.get(slug='sub-category-1b')
        self.assertTrue(not cat.has_children(), 'Category reporting children when it has no sub-categories.')

    def test_document_count(self):
        categories = models.DocumentCategory.objects.all()
        for cat in categories:
            self.assertEqual(cat.document_count(), 0, 'Category with no documents returns non-zero document_count.')


class DocumentTests(TestCase):
    """
        Test basic behaviours for Document model
    """
    def setUp(self):
        super().setUp()
        self.categories=base.create_document_categories()
        self.document = base.create_document(filename='myDocument.txt', file_type='txt')

    def test_get_absolute_url(self):
        self.assertIn(str(self.document.pk), self.document.get_absolute_url(), 'URL for document should contain its pk.')

    def test_get_filetype(self):
        filetype = self.document.get_filetype()
        self.assertEqual(filetype, 'txt', 'get_filetype returns incorrect type %s'%filetype)


class ConstrainedfileFieldTests(TestCase):
    """
        A few basic tests for fields.ConstrainedFileField -- ASSUMED to be field type for models.Document.file!
    """
    def setUp(self):
        super().setUp()
        self.categories=base.create_document_categories()

    def test_validation_success(self):
        document = base.create_document(filename='dummy.txt', file_type='txt')
        file_field = document.file.field
        self.assertIsNotNone(file_field.clean(value=document.file, model_instance=document))

    def test_max_upload_size_fail(self):
        document = base.create_document()
        file_field = document.file.field
        # hack the max_upload_size for test
        save_max = file_field.max_upload_size
        file_field.max_upload_size = 1
        with self.assertRaises(forms.ValidationError):
            file_field.clean(value=document.file, model_instance=document)
        file_field.max_upload_size = save_max

    def test_content_types_fail(self):
        document = base.create_document(filename='dummy.html', file_type='html')
        file_field = document.file.field
        with self.assertRaises(forms.ValidationError):
            file_field.clean(value=document.file, model_instance=document)
