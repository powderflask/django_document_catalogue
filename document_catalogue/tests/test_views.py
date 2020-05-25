import os

from django.test import TestCase
from django.urls import reverse
from document_catalogue import models, permissions
from . import base


class BaseTestWithUsers(TestCase):
    """
        Test behaviours for Document CRUD views
    """
    def setUp(self):
        super().setUp()
        self.categories = base.create_document_categories()
        self.privilegedUser = base.create_user(username='privileged',
                                               permissions=('Can add document', 'Can change document', 'Can delete document'))
        self.restrictedUser = base.create_user(username='restricted')

    def login(self, user):
        response = self.client.login(username=user.username, password='password')
        self.assertTrue(response)


class PermissionsTests(BaseTestWithUsers):
    """
    Test default permissions
    """
    def test_user_can_view_document_catalogue(self):
        self.assertFalse(permissions.user_can_view_document_catalogue(base.anonymous_user()))
        self.assertTrue(permissions.user_can_view_document_catalogue(self.restrictedUser))

    def test_user_can_download_document(self):
        self.assertFalse(permissions.user_can_download_document(base.anonymous_user()))
        self.assertTrue(permissions.user_can_download_document(self.restrictedUser))

    def test_user_can_edit_document(self):
        self.assertFalse(permissions.user_can_edit_document(self.restrictedUser))
        self.assertTrue(permissions.user_can_edit_document(self.privilegedUser))

    def test_user_can_post_document(self):
        self.assertFalse(permissions.user_can_post_document(self.restrictedUser))
        self.assertTrue(permissions.user_can_post_document(self.privilegedUser))

    def test_user_can_delete_document(self):
        self.assertFalse(permissions.user_can_delete_document(self.restrictedUser))
        self.assertTrue(permissions.user_can_delete_document(self.privilegedUser))


class SuccessDocumentViewTests(BaseTestWithUsers) :
    """
        SUCCESS -- test privileged user makes perfectly reasonable requests
    """
    def test_catalogue_list_view(self):
        self.login(self.restrictedUser)   # Any logged-in user can view the catalogue, by default
        url = reverse('document_catalogue:catalogue_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "Catalogue view returned non-success status code.")

    def test_category_list_view(self):
        self.login(self.restrictedUser)   # Any logged-in user can view the catalogue, by default
        category_slug = self.categories[0].slug
        url = reverse('document_catalogue:category_list', kwargs={'slug': category_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "Category view returned non-success status code.")

    def test_document_detail_view(self):
        self.login(self.restrictedUser)   # Any logged-in user can view docuemnts in the catalogue, by default
        document = base.create_document()
        url = reverse('document_catalogue:document_detail', kwargs={'pk': document.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "Document detail view returned non-success status code.")

    def test_document_download_view(self):
        self.login(self.restrictedUser)   # Any logged-in user can view docuemnts in the catalogue, by default
        document = base.create_document()
        url = reverse('document_catalogue:document_download', kwargs={'pk': document.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, "Document download view should re-direct and respond with file.")
        self.assertEqual(302, response.redirect_chain[0][1])
        self.assertIn(document.file.url, response.redirect_chain[0][0])


    def test_document_edit_view_get(self):
        self.login(self.privilegedUser)   # Only privileged users can edit a document
        document = base.create_document()
        url = reverse('document_catalogue:document_edit', kwargs={'pk': document.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "Get document edit view returned non-success status code.")

    def test_document_edit_view_post_errors(self) :
        self.login(self.privilegedUser)   # Only privileged users can edit a document
        document = base.create_document()

        myfile = base.generate_file('Test.txt', file_type='txt')
        with open(myfile.name, 'r') as file:
            new_title = 'A Brave New World!'
            post_data = {'file': file, 'title': new_title}  # missing required category
            url = reverse('document_catalogue:document_edit', kwargs={'pk': document.pk})
            response = self.client.post(url, data=post_data)
            self.assertEqual(response.status_code, 200, "Post to document edit view returned non-success status code.")
            self.assertIn(b'form-group has-error', response.content, "Invalid post data response does not contain form-errors")
        # Cleanup
        os.remove(myfile.name)

    def test_document_edit_view_post_success(self):
        self.login(self.privilegedUser)   # Only privileged users can edit a document
        document = base.create_document()
        new_title = 'A Brave New World!'

        myfile = base.generate_file('Test.txt', file_type='txt')
        with open(myfile.name, 'r') as file:
            post_data = {'file': file, 'title': new_title,
                         'description': 'new description', 'category': document.category.pk,
                         'is_published': ''}
            url = reverse('document_catalogue:document_edit', kwargs={'pk': document.pk})
            response = self.client.post(url, data=post_data)
            self.assertEqual(response.status_code, 302, "Post Document edit view did not redirect after editing doc.")
            self.assertNotIn(b'form-errors', response.content, "Valid post data response contains form-errors")

        doc = models.Document.objects.get(pk=document.pk)
        self.assertEqual(doc.title, new_title, "Valid post to document edit view did not alter the title")
        # Cleanup
        os.remove(myfile.name)

    def test_document_delete_view_get(self):
        self.login(self.privilegedUser)   # Only privileged users can delete a document
        document = base.create_document()
        url = reverse('document_catalogue:document_delete', kwargs={'pk': document.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "Get Document delete view returned non-success status code.")

    def test_document_delete_view_post(self):
        self.login(self.privilegedUser)   # Only privileged users can delete a document
        document = base.create_document()
        url = reverse('document_catalogue:document_delete', kwargs={'pk': document.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302, "Post Document delete view did not redirect after deleting doc.")
        with self.assertRaises(models.Document.DoesNotExist, msg="Document still exists after requesting delete URL."):
            models.Document.objects.get(pk=document.pk)


class DeniedDocumentViewTests(BaseTestWithUsers) :
    """
        DENIED -- test under-privileged user or otherwise makes unreasonable requests
    """
    def test_catalogue_list_view(self):
        # Only authenticated users can view the catalogue
        url = reverse('document_catalogue:catalogue_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403, "Catalogue view non-denied status code for anonymous user.")

    def test_category_list_view(self):
        # Only authenticated users can view the catalogue
        category_slug = self.categories[0].slug
        url = reverse('document_catalogue:category_list', kwargs={'slug': category_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403, "Category view non-denied status code for anonymous user.")

    def test_document_detail_view(self):
        # Only authenticated users can view the catalogue
        document = base.create_document()
        url = reverse('document_catalogue:document_detail', kwargs={'pk': document.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403, "Document detail view non-denied status code for anonymous user.")

    def test_document_download_view(self):
        # Only authenticated users can download documents
        document = base.create_document()
        url = reverse('document_catalogue:document_download', kwargs={'pk': document.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403, "Document download view non-denied status code for anonymous user.")

    def test_private_file_download(self):
        # Only authenticated users can download a document file
        document = base.create_document()
        response = self.client.get(document.file.url)
        self.assertEqual(response.status_code, 403, "Private file download view non-denied status code for anonymous user.")

    def test_document_edit_view(self):
        self.login(self.restrictedUser)   # Only privileged users can edit a document
        document = base.create_document()
        url = reverse('document_catalogue:document_edit', kwargs={'pk': document.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403, "Document edit view non-denied status code for restricted user.")

    def test_document_delete_view(self):
        self.login(self.restrictedUser)   # Only privileged users can delete a document
        document = base.create_document()
        url = reverse('document_catalogue:document_delete', kwargs={'pk': document.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403, "Document delete view non-denied status code for restricted user.")


class SuccessAjaxApiTests(BaseTestWithUsers) :
    """
        SUCCESS -- test privileged user makes perfectly reasonable requests
    """
    def test_api_post(self):
        self.login(self.privilegedUser)
        category_slug = self.categories[0].slug
        url = reverse('document_catalogue:api_post', kwargs={'slug': category_slug})
        myfile = base.generate_file('Test.txt', file_type='txt')
        with open(myfile.name, 'r') as file:
            post_data = {'file': file}
            response = self.client.post(url, post_data)
            self.assertEqual(response.status_code, 200, "Request to upload document file returned non-success status code.")
            self.assertEqual(models.Document.objects.count(), 1, "Document count incorrect after file upload.")

        document = models.Document.objects.all().first()
        _, filename = os.path.split(myfile.name)
        self.assertEqual(document.title, filename, "Document has different default name from uploaded file.")
        self.assertIn(category_slug, document.file.path, "Document path does not include category slug.")
        # The filename may get altered when saved, but should contain the name and extension of the original
        name, extension = os.path.splitext(filename)
        self.assertIn(name, document.file.path, "Document path does not contain original uploaded file name.")
        self.assertIn(extension, document.file.path, "Document path does not contain original uploaded file name.")
        # Cleanup
        os.remove(myfile.name)

    def test_api_delete(self):
        self.login(self.privilegedUser)   # Only privileged users can delete a document
        document = base.create_document()
        url = reverse('document_catalogue:api_delete', kwargs={'pk': document.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200, "Request to delete document returned non-success status code.")
        with self.assertRaises(models.Document.DoesNotExist, msg="Document still exists after requesting delete URL."):
            models.Document.objects.get(pk=document.pk)


class DeniedAjaxApiTests(BaseTestWithUsers) :
    """
        DENIED -- test unprivileged user or otherwise makes unreasonable requests
    """
    def test_api_post_invalid_file(self):
        self.login(self.privilegedUser)
        category_slug = self.categories[0].slug
        url = reverse('document_catalogue:api_post', kwargs={'slug': category_slug})

        myfile = base.generate_file('Test.html', file_type='html')
        with open(myfile.name, 'r') as file:
            post_data = {'file': file}
            response = self.client.post(url, post_data)
            self.assertEqual(response.status_code, 403, "Invalid filetype did not result in PermissionDenied.")
        # Cleanup
        os.remove(myfile.name)

    def test_api_post(self):
        self.login(self.restrictedUser)   # Only privileged users can delete a document
        category_slug = self.categories[0].slug
        url = reverse('document_catalogue:api_post', kwargs={'slug': category_slug})

        myfile = base.generate_file('Test.txt', file_type='txt')
        with open(myfile.name, 'r') as file:
            post_data = {'file': file}
            response = self.client.post(url, post_data)
            self.assertEqual(response.status_code, 403, "Request to upload file non-denied status code for restricted user.")
        # Cleanup
        os.remove(myfile.name)

    def test_api_delete(self):
        self.login(self.restrictedUser)   # Only privileged users can delete a document
        document = base.create_document()
        url = reverse('document_catalogue:api_delete', kwargs={'pk': document.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, "Request to delete document non-denied status code for restricted user.")
