from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", publication_year=2020, author=self.author
        )

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        url = reverse("book-list")
        data = {"title": "New Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book(self):
        url = reverse("book-detail", args=[self.book.id])
        data = {"title": "Updated Title", "publication_year": 2019, "author": self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
# api/test_views.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Author, Book
from datetime import date

class BookAPITests(APITestCase):
    """
    Tests for the Book API endpoints including CRUD, Filtering, Searching, and Ordering.
    """
    def setUp(self):
        """
        Set up test data and users for all tests.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author1 = Author.objects.create(name="Jane Austen")
        self.author2 = Author.objects.create(name="George Orwell")
        self.book1 = Book.objects.create(
            title="Pride and Prejudice", publication_year=1813, author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Sense and Sensibility", publication_year=1811, author=self.author1
        )
        self.book3 = Book.objects.create(
            title="1984", publication_year=1949, author=self.author2
        )
        self.book_list_url = reverse('book-list-create')
        self.book_detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})

        print(f"\n--- Setting up BookAPITests ---")
        print(f"User: {self.user.username}")
        print(f"Authors: {Author.objects.count()}")
        print(f"Books: {Book.objects.count()}")
        print(f"BookList URL: {self.book_list_url}")

    def test_list_books_unauthenticated(self):
        """
        Ensure unauthenticated users can list books (read-only).
        """
        print("\nRunning: test_list_books_unauthenticated")
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3) # Expecting 3 books
        self.assertIn(self.book1.title, [book['title'] for book in response.data])

    def test_create_book_unauthenticated(self):
        """
        Ensure unauthenticated users cannot create books.
        """
        print("\nRunning: test_create_book_unauthenticated")
        data = {'title': 'New Book', 'publication_year': 2020, 'author': self.author1.id}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3) # No new book created

    def test_create_book_authenticated(self):
        """
        Ensure authenticated users can create books.
        """
        print("\nRunning: test_create_book_authenticated")
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Brave New World', 'publication_year': 1932, 'author': self.author2.id}
        response = self.client.post(self.book_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.last().title, 'Brave New World')

    def test_create_book_with_future_publication_year_authenticated(self):
        """
        Ensure creating a book with a future publication year fails validation.
        """
        print("\nRunning: test_create_book_with_future_publication_year_authenticated")
        self.client.force_authenticate(user=self.user)
        future_year = date.today().year + 1
        data = {'title': 'Future Book', 'publication_year': future_year, 'author': self.author1.id}
        response = self.client.post(self.book_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertIn('Publication year cannot be in the future.', response.data['publication_year'])

    def test_retrieve_book(self):
        """
        Ensure a specific book can be retrieved.
        """
        print("\nRunning: test_retrieve_book")
        response = self.client.get(self.book_detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_update_book_unauthenticated(self):
        """
        Ensure unauthenticated users cannot update books.
        """
        print("\nRunning: test_update_book_unauthenticated")
        data = {'title': 'Updated Title', 'publication_year': 1813, 'author': self.author1.id}
        response = self.client.put(self.book_detail_url(self.book1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Updated Title')

    def test_update_book_authenticated(self):
        """
        Ensure authenticated users can update books.
        """
        print("\nRunning: test_update_book_authenticated")
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Pride and Prejudice', 'publication_year': 1813, 'author': self.author1.id}
        response = self.client.put(self.book_detail_url(self.book1.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Pride and Prejudice')

    def test_delete_book_unauthenticated(self):
        """
        Ensure unauthenticated users cannot delete books.
        """
        print("\nRunning: test_delete_book_unauthenticated")
        response = self.client.delete(self.book_detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists()) # Book still exists

    def test_delete_book_authenticated(self):
        """
        Ensure authenticated users can delete books.
        """
        print("\nRunning: test_delete_book_authenticated")
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists()) # Book is deleted

    # --- Filtering, Searching, Ordering Tests ---

    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication_year.
        """
        print("\nRunning: test_filter_books_by_publication_year")
        response = self.client.get(self.book_list_url + '?publication_year=1949')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book3.title)

    def test_filter_books_by_title_icontains(self):
        """
        Test filtering books by title (case-insensitive contains).
        """
        print("\nRunning: test_filter_books_by_title_icontains")
        response = self.client.get(self.book_list_url + '?title=pride')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book1.title)

    def test_filter_books_by_author_name_icontains(self):
        """
        Test filtering books by author name (case-insensitive contains).
        """
        print("\nRunning: test_filter_books_by_author_name_icontains")
        response = self.client.get(self.book_list_url + '?author_name=jane')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        titles = [book['title'] for book in response.data]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)

    def test_search_books_by_title_or_author(self):
        """
        Test searching books by title or author name.
        """
        print("\nRunning: test_search_books_by_title_or_author")
        response = self.client.get(self.book_list_url + '?search=1984')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book3.title)

        response = self.client.get(self.book_list_url + '?search=austen') # Search for author name
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        titles = [book['title'] for book in response.data]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)

    def test_order_books_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        """
        print("\nRunning: test_order_books_by_title_descending")
        response = self.client.get(self.book_list_url + '?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        # Expected order: Sense and Sensibility, Pride and Prejudice, 1984 (alphabetical desc)
        self.assertEqual(titles[0], self.book2.title) # Sense and Sensibility
        self.assertEqual(titles[1], self.book1.title) # Pride and Prejudice
        self.assertEqual(titles[2], self.book3.title) # 1984

    def test_order_books_by_publication_year_ascending(self):
        """
        Test ordering books by publication_year in ascending order.
        """
        print("\nRunning: test_order_books_by_publication_year_ascending")
        response = self.client.get(self.book_list_url + '?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        # Expected order: Sense and Sensibility (1811), Pride and Prejudice (1813), 1984 (1949)
        self.assertEqual(titles[0], self.book2.title)
        self.assertEqual(titles[1], self.book1.title)
        self.assertEqual(titles[2], self.book3.title)

class AuthorAPITests(APITestCase):
    """
    Tests for the Author API endpoints including CRUD.
    """
    def setUp(self):
        """
        Set up test data and users.
        """
        self.user = User.objects.create_user(username='testuser2', password='testpassword2')
        self.author1 = Author.objects.create(name="Virginia Woolf")
        self.author2 = Author.objects.create(name="F. Scott Fitzgerald")
        Book.objects.create(title="Mrs Dalloway", publication_year=1925, author=self.author1)
        Book.objects.create(title="The Great Gatsby", publication_year=1925, author=self.author2)

        self.author_list_url = reverse('author-list-create')
        self.author_detail_url = lambda pk: reverse('author-detail', kwargs={'pk': pk})

        print(f"\n--- Setting up AuthorAPITests ---")