from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookViewTests(APITestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpass")

        # Create a book owned by testuser
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="A test book description",
            owner=self.user,
            is_published=True
        )

    def test_book_list_authenticated(self):
        """Authenticated users can view book list"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])  # ✅ check response data
        self.assertEqual(response.data[0]["title"], "Test Book")

    def test_book_create_authenticated(self):
        """Authenticated user can create a book"""
        self.client.login(username="testuser", password="testpass")
        data = {
            "title": "Another Test Book",
            "author": "Another Author",
            "description": "Another description",
            "is_published": True,
        }
        response = self.client.post(reverse("book-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Another Test Book")  # ✅ confirm response content
        self.assertEqual(Book.objects.count(), 2)

    def test_book_create_unauthenticated(self):
        """Unauthenticated users cannot create a book"""
        data = {
            "title": "Unauthorized Book",
            "author": "No Author",
            "description": "Should not be created",
            "is_published": True,
        }
        response = self.client.post(reverse("book-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_update_authenticated_owner(self):
        """Owner can update their book"""
        self.client.login(username="testuser", password="testpass")
        url = reverse("book-update", args=[self.book.pk])
        data = {
            "title": "Updated Test Book",
            "author": "Updated Author",
            "description": "Updated description",
            "is_published": True,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Test Book")  # ✅ check response payload
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Test Book")

    def test_book_update_authenticated_not_owner(self):
        """Non-owner cannot update the book"""
        self.client.login(username="otheruser", password="otherpass")
        url = reverse("book-update", args=[self.book.pk])
        data = {
            "title": "Hacker Update",
            "author": "Not Owner",
            "description": "This should fail",
            "is_published": True,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)  # ✅ confirm error message

    def test_book_delete_authenticated_owner(self):
        """Owner can delete their book"""
        self.client.login(username="testuser", password="testpass")
        url = reverse("book-delete", args=[self.book.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_book_delete_authenticated_not_owner(self):
        """Non-owner cannot delete the book"""
        self.client.login(username="otheruser", password="otherpass")
        url = reverse("book-delete", args=[self.book.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)  # ✅ confirm error response
        self.assertEqual(Book.objects.count(), 1)
