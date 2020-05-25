import os

from django.conf import settings as django_settings
from django.test import TestCase
from django.core.files.uploadedfile import UploadedFile
from django import forms
from document_catalogue import models, settings
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
        self.assertIn(django_settings.PRIVATE_STORAGE_ROOT, self.document.file.path)


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
        # fudge the file size to exceed max.
        file_size = settings.DOCUMENT_CATALOGUE_MAX_FILESIZE + 1
        document.file.file = \
            UploadedFile(file=document.file.file, name=document.title, content_type='txt', size=file_size)
        with self.assertRaises(forms.ValidationError):
            file_field.clean(value=document.file, model_instance=document)
        # Cleanup
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
