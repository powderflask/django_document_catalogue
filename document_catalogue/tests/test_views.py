import os
from importlib import import_module

from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from document_catalogue import settings, models, views
from . import base
permissions = import_module(settings.DOCUMENT_CATALOGUE_PERMISSIONS)

# Create tests for views here.

class DocumentCrudViewTests(TestCase):
    """
        Test behaviours for Docuent CRUD views
    """
    def setUp(self):
        super().setUp()
        self.categories=base.create_document_categories()
        self.privilegedUser = base.create_user(username='privileged',
                                               permissions=('Can add document', 'Can change document', 'Can delete document'))
        self.assertTrue(permissions.user_can_post_document(self.privilegedUser))
        self.restrictedUser = base.create_user(username='restricted')
        self.assertFalse(permissions.user_can_post_document(self.restrictedUser))

    def login(self, user):
        response = self.client.login(username=user.username, password='password')
        self.assertTrue(response)

    def test_file_upload(self):
        self.login(self.privilegedUser)

        myfile = base.generate_file('Test.txt', file_type='txt')
        file_path = myfile.name
        f = open(file_path, "r")

        category_slug = self.categories[0].slug
        url = reverse('document_catalogue_ajax_post', kwargs={'slug':category_slug})

        post_data = {'file': f}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200, "Request to upload document file returned non-success status code.")
        self.assertEqual(models.Document.objects.count(), 1, "Document count incorrect after file upload.")

        document = models.Document.objects.all().first()
        self.assertEqual(document.title, myfile.name, "Document has different default name from uploaded file.")
        self.assertIn(category_slug, document.file.path, "Document path does not include category slug.")
        self.assertIn(myfile.name, document.file.path, "Document path does not contain origial uploaded file name.")

        # Cleanup
        os.remove(myfile.name)
        file_path = document.file.path
        os.remove(file_path)

    def test_invalid_file_type_upload(self):
        self.login(self.privilegedUser)

        myfile = base.generate_file('Test.html', file_type='html')
        file_path = myfile.name
        f = open(file_path, "r")

        category_slug = self.categories[0].slug
        url = reverse('document_catalogue_ajax_post', kwargs={'slug':category_slug})

        post_data = {'file': f}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 403, "Invalid filetype did not result in PermissionDenied.")

        # Cleanup
        os.remove(myfile.name)
