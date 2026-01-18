from django.contrib import admin
from django.urls import path
from cart_api.views import add_to_cart, view_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cart/add/', add_to_cart, name='add_to_cart'),
    path('api/cart/<int:user_id>/', view_cart, name='view_cart'),
]