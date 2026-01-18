from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem
import json
import requests # Thư viện để gọi API sang service khác

BOOK_SERVICE_URL = "http://127.0.0.1:8001/api/books/"

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        book_id = data.get('book_id')
        
        # 1. GIAO TIẾP MICROSERVICE: Gọi sang Book Service để check sách và lấy giá
        try:
            response = requests.get(f"{BOOK_SERVICE_URL}{book_id}/")
            if response.status_code != 200:
                return JsonResponse({'error': 'Book service unavailable or Book not found'}, status=404)
            book_data = response.json()
        except:
             return JsonResponse({'error': 'Cannot connect to Book Service'}, status=503)

        # 2. Xử lý logic giỏ hàng (Local)
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        item, created = CartItem.objects.get_or_create(cart=cart, book_id=book_id)
        
        if not created:
            item.quantity += 1
        else:
            item.quantity = 1
            item.price = book_data['price'] # Lưu giá lấy từ Service kia
            
        item.save()
        return JsonResponse({'message': 'Added to cart', 'cart_id': cart.id})

def view_cart(request, user_id):
    try:
        cart = Cart.objects.get(user_id=user_id)
        items = CartItem.objects.filter(cart=cart)
        
        result = []
        total = 0
        for item in items:
            # Ở đây nếu kỹ tính thì gọi lại Book Service để lấy Tên sách mới nhất
            # Nhưng để demo nhanh, ta trả về book_id thôi
            subtotal = item.quantity * item.price
            total += subtotal
            result.append({
                'book_id': item.book_id,
                'quantity': item.quantity,
                'price': float(item.price),
                'subtotal': float(subtotal)
            })
            
        return JsonResponse({'user_id': user_id, 'items': result, 'total': float(total)})
    except Cart.DoesNotExist:
        return JsonResponse({'items': [], 'total': 0})