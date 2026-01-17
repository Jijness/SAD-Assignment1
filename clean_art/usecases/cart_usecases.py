from interfaces.repositories import CartRepositoryInterface

class AddToCartUseCase:
    def __init__(self, repo: CartRepositoryInterface):
        self.repo = repo
    def execute(self, user_id, book_id):
        self.repo.add_item(user_id, book_id)

class ListCartUseCase:
    def __init__(self, repo: CartRepositoryInterface):
        self.repo = repo
    def execute(self, user_id):
        return self.repo.get_cart_items(user_id)

class RemoveItemUseCase:
    def __init__(self, repo: CartRepositoryInterface):
        self.repo = repo
    def execute(self, user_id, item_id):
        self.repo.remove_item(user_id, item_id)