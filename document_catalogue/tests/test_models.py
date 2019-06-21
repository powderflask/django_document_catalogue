from django.test import TestCase, SimpleTestCase
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
