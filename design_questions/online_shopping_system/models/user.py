import uuid
from typing import List

class User:
    def __init__(self,id:str,name:str,email:str,order_history:List[str]):
        self.id = id
        self.name = name
        self.email = email
        self.order_history = order_history
