# Import từ các file con ra ngoài để urls.py chỉ cần gọi app.views
from .book_views import book_list, book_detail
from .cart_views import add_to_cart, view_cart, remove_from_cart
from .auth_views import register