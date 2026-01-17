from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
# Import TẤT CẢ các view thật
from app.views import (
    book_list, book_detail, register, 
    add_to_cart, view_cart, remove_from_cart
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- SÁCH ---
    path('', book_list, name='book_list'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
    
    # --- CART (Đã dùng Clean Architecture) ---
    path('cart/', view_cart, name='view_cart'),
    path('add-to-cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    
    # --- AUTHENTICATION (Dùng Framework views) ---
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', register, name='register'),
]