from typing import List
from models.product import Product

class InventoryService:
    def __init__(self,products:List[Product]):
        self.inventory = products
    
    
    def is_available(self,product:Product,quantity:int):
        return product.quantity_available >= quantity
