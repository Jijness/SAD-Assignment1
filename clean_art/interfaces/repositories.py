from abc import ABC, abstractmethod
from typing import List
from domain.entities import BookEntity

class BookRepositoryInterface(ABC):
    @abstractmethod
    def get_all_books(self) -> List[BookEntity]:
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> BookEntity:
        pass
    
    @abstractmethod
    def search_books(self, query: str) -> List[BookEntity]:
        pass

class CartRepositoryInterface(ABC):
    @abstractmethod
    def add_item(self, user_id: int, book_id: int):
        pass

    @abstractmethod
    def get_cart_items(self, user_id: int):
        pass

    @abstractmethod
    def remove_item(self, user_id: int, item_id: int):
        pass