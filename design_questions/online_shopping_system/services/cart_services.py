from typing import List
from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
from services.inventory_service import InventoryService
import uuid

class CartService:
    def __init__(self,inventory_service:InventoryService):
        
    