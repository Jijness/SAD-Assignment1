from django.contrib import admin
from .models import BookModel # Nhớ là BookModel nhé
admin.site.register(BookModel)