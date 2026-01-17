from django.db.models import Q
from typing import List
from interfaces.repositories import BookRepositoryInterface, CartRepositoryInterface
from domain.entities import BookEntity, CartItemEntity
from app.models import BookModel, CartModel, CartItemModel


# Đây là class thực hiện công việc "bẩn" (chọc vào DB)
class DjangoBookRepository(BookRepositoryInterface):
    
    def get_all_books(self) -> List[BookEntity]:
        # 1. Dùng Django ORM lấy dữ liệu từ DB
        book_models = BookModel.objects.all()
        
        # 2. CHUYỂN ĐỔI (Mapping): Django Model -> Domain Entity
        entities = []
        for model in book_models:
            entities.append(BookEntity(
                id=model.id,
                title=model.title,
                author=model.author,
                price=float(model.price),
                stock=model.stock
            ))
        return entities

    def get_book_by_id(self, book_id: int) -> BookEntity:
        model = BookModel.objects.get(id=book_id)
        return BookEntity(
            id=model.id,
            title=model.title,
            author=model.author,
            price=float(model.price),
            stock=model.stock
        )
    
    def search_books(self, query: str) -> List[BookEntity]:
        # Dùng Django ORM để lọc
        models = BookModel.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        
        # Convert sang Entity
        return [
            BookEntity(
                id=m.id, title=m.title, author=m.author, 
                price=float(m.price), stock=m.stock
            ) for m in models
        ]
    
class DjangoCartRepository(CartRepositoryInterface):
    
    def add_item(self, user_id: int, book_id: int):
        # Logic: Tìm giỏ -> Tìm sách -> Tìm Item -> +1 hoặc tạo mới
        cart, _ = CartModel.objects.get_or_create(user_id=user_id)
        book = BookModel.objects.get(id=book_id)
        
        item, created = CartItemModel.objects.get_or_create(cart=cart, book=book)
        if not created:
            item.quantity += 1
            item.save()
        else:
            item.quantity = 1
            item.save()

    def get_cart_items(self, user_id: int):
        cart, _ = CartModel.objects.get_or_create(user_id=user_id)
        models = CartItemModel.objects.filter(cart=cart)
        
        # Convert Django Model -> Domain Entity để trả về cho View
        entities = []
        for m in models:
            book_entity = BookEntity(
                id=m.book.id, title=m.book.title, author=m.book.author,
                price=float(m.book.price), stock=m.book.stock
            )
            entities.append(CartItemEntity(book=book_entity, quantity=m.quantity))
            # Hack nhẹ: Gán thêm id của item vào entity để dùng cho nút xóa
            entities[-1].id = m.id 
        return entities

    def remove_item(self, user_id: int, item_id: int):
        try:
            # Đảm bảo user chỉ xóa được item trong giỏ của mình
            item = CartItemModel.objects.get(id=item_id, cart__user_id=user_id)
            item.delete()
        except CartItemModel.DoesNotExist:
            pass