from django.shortcuts import render, redirect
from infrastructure.repositories import DjangoBookRepository
from usecases.book_usecases import ListBooksUseCase, SearchBooksUseCase, ViewBookDetailUseCase

def book_list(request):
    query = request.GET.get('q')
    if query == '':
        return redirect('book_list')
    # 1. Khởi tạo Repository (công cụ lấy DB)
    repo = DjangoBookRepository()
    # 2. Điều hướng Use Case: Có query thì Tìm, không thì Lấy hết
    if query:
        # Nếu đang tìm kiếm -> Gọi ông Search Use Case
        use_case = SearchBooksUseCase(repo)
        books = use_case.execute(query)
    else:
        # Nếu xem thường -> Gọi ông List Use Case
        use_case = ListBooksUseCase(repo)
        books = use_case.execute()
    # 3. Trả về template (Dùng lại của Monolith vẫn OK)
    # Truyền thêm biến 'query' để ô input giữ lại chữ vừa gõ
    return render(request, 'book_list.html', {'books': books, 'query': query})

def book_detail(request, pk):
    repo = DjangoBookRepository()
    use_case = ViewBookDetailUseCase(repo)
    # Thực thi Use Case
    book = use_case.execute(pk)
    return render(request, 'book_detail.html', {'book': book})