from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from books.models import Book

@login_required(login_url='login') # Bắt buộc đăng nhập mới được mua
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Lấy hoặc tạo giỏ hàng cho user hiện tại
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Kiểm tra sách này đã có trong giỏ chưa
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        # Nếu có rồi thì tăng số lượng lên 1
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Nếu chưa có thì set số lượng là 1 (mặc định model đã set, nhưng cứ gán cho chắc)
        cart_item.quantity = 1
        cart_item.save()
    
    return redirect('view_cart')

@login_required(login_url='login')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all() # Lấy tất cả item trong giỏ
    
    # Tính tổng tiền (Python tính toán trực tiếp)
    total_price = sum(item.book.price * item.quantity for item in items)
    
    return render(request, 'cart.html', {'items': items, 'total_price': total_price})

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    # Chỉ cho phép xóa item của chính user đó (bảo mật)
    if item.cart.user == request.user:
        item.delete()
    return redirect('view_cart')