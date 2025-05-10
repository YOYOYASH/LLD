from models.product import Product


class OrderItem:
    def __init__(self,product:Product,quantity:int,price:float):
        self.product = product
        self.quantity = quantity
        self.price = price

        