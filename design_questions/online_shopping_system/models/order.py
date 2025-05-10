from enum import Enum
from models.order_item import OrderItem
from models.user import User

from typing import List

class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order:
    def __init__(self,id:str,user:User,cart_items:List[OrderItem]):
        self.id = id
        self.user = user
        self.items = [
            OrderItem(item.product,item.quantity,item.product.price)
            for item in cart_items
        ]
        
    def calculate_checkout_total(self):
        return sum(item.price * item.quantity for item in self.items)