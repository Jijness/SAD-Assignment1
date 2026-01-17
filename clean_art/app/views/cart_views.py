from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from infrastructure.repositories import DjangoCartRepository
from usecases.cart_usecases import AddToCartUseCase, ListCartUseCase, RemoveItemUseCase

@login_required(login_url='login')
def add_to_cart(request, book_id):
    repo = DjangoCartRepository()
    use_case = AddToCartUseCase(repo)
    use_case.execute(request.user.id, book_id)
    return redirect('view_cart')

@login_required(login_url='login')
def view_cart(request):
    repo = DjangoCartRepository()
    use_case = ListCartUseCase(repo)
    items = use_case.execute(request.user.id)
    
    # Tính tổng tiền (Logic hiển thị)
    total_price = sum(item.book.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total_price': total_price})

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    repo = DjangoCartRepository()
    use_case = RemoveItemUseCase(repo)
    use_case.execute(request.user.id, item_id)
    return redirect('view_cart')