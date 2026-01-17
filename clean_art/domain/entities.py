from dataclasses import dataclass
from typing import Optional

# Đây là Entity, không phải Django Model!
@dataclass
class BookEntity:
    id: Optional[int]
    title: str
    author: str
    price: float
    stock: int

@dataclass
class CartItemEntity:
    book: BookEntity
    quantity: int

    @property
    def total_price(self):
        return self.price * self.quantity