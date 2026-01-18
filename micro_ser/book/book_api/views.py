from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book
import json

# API 1: Lấy danh sách sách
def get_books(request):
    books = Book.objects.all()
    # Chuyển đổi dữ liệu sang dạng List of Dictionaries (JSON)
    data = list(books.values('id', 'title', 'author', 'price', 'stock'))
    return JsonResponse(data, safe=False)

# API 2: Lấy chi tiết 1 cuốn sách
def get_book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price), # Decimal không serialize được, phải ép kiểu float
            'stock': book.stock
        }
        return JsonResponse(data)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

# API 3: Giảm tồn kho (Dành cho Cart Service gọi khi mua hàng)
@csrf_exempt # Tắt bảo mật CSRF để service khác gọi được POST
def reduce_stock(request, pk):
    if request.method == 'POST':
        try:
            book = Book.objects.get(pk=pk)
            data = json.loads(request.body) # Lấy dữ liệu gửi lên
            quantity = data.get('quantity', 1)
            
            if book.stock >= quantity:
                book.stock -= quantity
                book.save()
                return JsonResponse({'message': 'Stock updated', 'new_stock': book.stock})
            else:
                return JsonResponse({'error': 'Out of stock'}, status=400)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)