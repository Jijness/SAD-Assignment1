from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.db.models import Q

def book_list(request):
    query = request.GET.get('q')
    if query == '':
        return redirect('book_list')

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books, 'query': query})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk) # Lấy sách theo ID (pk)
    return render(request, 'book_detail.html', {'book': book})