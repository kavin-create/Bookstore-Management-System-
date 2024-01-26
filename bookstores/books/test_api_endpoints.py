from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Book

class BookstoreAPITests(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some sample books for testing
        self.book1 = Book.objects.create(title='Book 1', author='Author 1', isbn='1234567890123', price=20.99, quantity=10)
        self.book2 = Book.objects.create(title='Book 2', author='Author 2', isbn='2345678901234', price=25.99, quantity=15)

        # Create an API client for making requests
        self.client = APIClient()

    def test_login_and_token_retrieval(self):
        # Test user login and token retrieval
        login_url = reverse('login')
        login_data = {'username': 'kavin', 'password': 'admin'}
        response = self.client.post(login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

        # Store the token for later use
        self.token = response.data['access_token']

    def test_add_new_book(self):
        # Test adding a new book
        url = reverse('book-list-create')
        data = {'title': 'New Book', 'author': 'New Author', 'isbn': '3456789012345', 'price': 19.99, 'quantity': 5}

        # Include the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_retrieve_all_books(self):
        # Test retrieving all books
        url = reverse('book-list-create')

        # Include the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming two books are created in setUp

    def test_retrieve_specific_book_by_isbn(self):
        # Test retrieving a specific book by ISBN
        isbn = '1234567890123'
        url = reverse('book-by-isbn', args=[isbn])

        # Include the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['isbn'], isbn)

    def test_update_book_details(self):
        # Test updating book details
        book_id = self.book1.id
        url = reverse('book-retrieve-update-delete', args=[book_id])
        data = {'title': 'Updated Title', 'price': 29.99}

        # Include the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.token)

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_book(self):
        # Test deleting a book
        book_id = self.book2.id
        url = reverse('book-retrieve-update-delete', args=[book_id])

        # Include the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

