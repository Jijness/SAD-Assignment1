from django.contrib import admin
from django.urls import path
from book_api.views import get_books, get_book_detail, reduce_stock

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', get_books, name='get_books'),
    path('api/books/<int:pk>/', get_book_detail, name='get_book_detail'),
    path('api/books/<int:pk>/reduce-stock/', reduce_stock, name='reduce_stock'),
]