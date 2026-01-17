from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Cart(models.Model):
    # Mỗi User chỉ có 1 giỏ hàng (OneToOne)
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.quantity * self.book.price