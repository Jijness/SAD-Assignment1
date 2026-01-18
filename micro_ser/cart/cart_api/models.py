from django.db import models

class Cart(models.Model):
    user_id = models.IntegerField(unique=True) # Chỉ lưu ID, không ForeinKey
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book_id = models.IntegerField() # Chỉ lưu ID sách
    quantity = models.IntegerField(default=1)
    
    # Ta lưu thêm giá tại thời điểm mua (Snapshot)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)