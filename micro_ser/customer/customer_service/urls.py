from django.contrib import admin
from django.urls import path
from user_api.views import register, login_view, get_user_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register, name='register'),
    path('api/login/', login_view, name='login'),
    path('api/users/<int:pk>/', get_user_detail, name='get_user_detail'),
]