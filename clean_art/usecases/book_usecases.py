from typing import List
from domain.entities import BookEntity
from interfaces.repositories import BookRepositoryInterface

class ListBooksUseCase:
    # Dependency Injection: Nhận vào một cái Repository bất kỳ (miễn là tuân thủ Interface)
    def __init__(self, book_repo: BookRepositoryInterface):
        self.book_repo = book_repo

    def execute(self) -> List[BookEntity]:
        # Logic nghiệp vụ: Chỉ đơn giản là lấy sách về
        return self.book_repo.get_all_books()
    
class ViewBookDetailUseCase:
    def __init__(self, book_repo: BookRepositoryInterface):
        self.book_repo = book_repo

    def execute(self, book_id: int) -> BookEntity:
        return self.book_repo.get_book_by_id(book_id)
    
class SearchBooksUseCase:
    def __init__(self, book_repo: BookRepositoryInterface):
        self.book_repo = book_repo

    def execute(self, query: str) -> List[BookEntity]:
        return self.book_repo.search_books(query)