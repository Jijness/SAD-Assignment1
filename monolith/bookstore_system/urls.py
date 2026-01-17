"""
URL configuration for bookstore_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from books.views import book_list, book_detail
from cart.views import add_to_cart, view_cart, remove_from_cart
from accounts.views import register

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- URL cho SÁCH ---
    path('', book_list, name='book_list'), # Trang chủ là danh sách sách
    path('book/<int:pk>/', book_detail, name='book_detail'),

    # --- URL cho TÀI KHOẢN ---
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # LogoutView mới cần set next_page để biết logout xong đi đâu
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # --- URL cho GIỎ HÀNG ---
    path('cart/', view_cart, name='view_cart'),
    path('add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]
