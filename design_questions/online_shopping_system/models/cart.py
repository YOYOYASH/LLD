from models.user import User
from models.product import Product
from models.cart_item import CartItem

class Cart:
    def __init__(self,id:str,user:User):
        self.id = id
        self.user = user
        self.items = {} # product_id -> CartItem

    def add_item(self,product:Product,quantity:int):
        if product.id in self.items:
            self.items[product.id].quantity += quantity
        else:
            self.items[product.id] = CartItem(product,quantity)
    
    def remove_item(self,product_id:int):
        if product_id in self.items:
            del self.items[product_id]
    
    def update_qunatity(self,product_id:int,quantity:int):
        if product_id in self.items:
            self.items[product_id].quantity = quantity
    
    def calculate_cart_total(self):
        return sum(item.product.price * item.quantity for item in self.items.values())
    
