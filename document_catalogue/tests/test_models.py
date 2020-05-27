import os

import django.conf
from django.test import TestCase
from django.core.files.uploadedfile import UploadedFile
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
            self.assertEqual(cat.get_document_count(), 0, 'Category with no documents returns non-zero get_document_count.')


class DocumentTests(TestCase):
    """
        Test basic behaviours for Document model
    """
    FILENAME = 'myDocument.txt'

    def setUp(self):
        super().setUp()
        self.categories=base.create_document_categories()
        self.document = base.create_document(filename=self.FILENAME, file_type='txt')

    def tearDown(self):
        os.remove(self.document.file.path)

    def test_get_absolute_url(self):
        self.assertIn(str(self.document.pk), self.document.get_absolute_url(), 'URL for document should contain its pk.')

    def test_get_filetype(self):
        filetype = self.document.get_filetype()
        self.assertEqual(filetype, 'txt', 'get_filetype returns incorrect type %s' % filetype)

    def test_document_directory_path(self):
        instance = lambda: None  # a mutable null object
        instance.category = self.categories[0]
        path = models.document_upload_path_callback(instance, self.FILENAME)
        self.assertIn(self.categories[0].slug, path)
        self.assertIn(self.FILENAME, path)

    def test_create_file(self):
        filename = 'slartibartfast.txt'
        file = base.create_document(filename=filename, file_type='txt', user=base.create_user(username='slartibartfast'))
        doc = models.Document.objects.get(pk=file.pk)
        self.assertIn(filename, doc.file.name)
        self.assertIn(filename, doc.file.url)
        # Cleanup
        os.remove(doc.file.path)

    def test_private_storage(self):
        media_root = getattr(django.conf.settings, 'PRIVATE_STORAGE_ROOT') if base.appConfig.USE_PRIVATE_FILES \
                                                                         else django.conf.settings.MEDIA_ROOT
        self.assertIn(media_root, self.document.file.path)
        self.assertIn(base.appConfig.settings.MEDIA_ROOT, self.document.file.path)


class ConstrainedfileFieldTests(TestCase):
    """
        A few basic tests for common validation in both PrivateFileField and ConstrainedFileField
    """
    def setUp(self):
        super().setUp()
        self.categories=base.create_document_categories()

    def test_validation_success(self):
        document = base.create_document(filename='dummy.txt', file_type='txt')
        file_field = document.file.field
        self.assertIsNotNone(file_field.clean(value=document.file, model_instance=document))

    class FileField:
        def __init__(self, field):
            self.field = field
            self.store = self.get_max_upload_size()
        def get_max_upload_size(self):
            return self.field.max_file_size if base.appConfig.USE_PRIVATE_FILES else self.field.max_upload_size
        def set_max_upload_size(self, max):
            self.field.max_upload_size = max
        def restore_max_upload_size(self):
            if base.appConfig.USE_PRIVATE_FILES:
                self.field.max_file_size = self.store
            else:
                self.field.max_upload_size = self.store

    def test_max_upload_size_fail(self):
        document = base.create_document()
        file_field = self.FileField(document.file.field)
        file_size = file_field.get_max_upload_size()-1
        document.file.file = \
            UploadedFile(file=document.file.file, name=document.title, content_type='txt', size=file_size)
        # fudge the max_upload_size to fall below file size.
        file_field.set_max_upload_size(document.file.size - 1)
        with self.assertRaises(forms.ValidationError):
            file_field.field.clean(value=document.file, model_instance=document)
        # Cleanup
        file_field.restore_max_upload_size()
        os.remove(document.file.path)

    def test_content_types_fail(self):
        document = base.create_document(filename='dummy.html', file_type='html')
        file_field = document.file.field
        document.file.file = \
            UploadedFile(file=document.file.file, name=document.title, content_type='html', size=document.file.size)
        with self.assertRaises(forms.ValidationError):
            file_field.clean(value=document.file, model_instance=document)
        # Cleanup
        os.remove(document.file.path)
