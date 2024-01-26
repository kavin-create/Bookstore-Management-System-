from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDeleteView, login, BookByISBNView

urlpatterns = [
    path('login/', login, name='login'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<str:isbn>/', BookRetrieveUpdateDeleteView.as_view(), name='book-retrieve-update-delete'),
    path('books/by-isbn/<str:isbn>/', BookByISBNView.as_view(), name='book-by-isbn'),
]
