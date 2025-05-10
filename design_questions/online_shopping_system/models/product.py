class ProductCategory:
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    BOOKS = "books"
    GROCERY = "grocery"

class Product:
    def __init__(self,id:str,name:str,description:str,price:float,quantity_available:int,category:ProductCategory):
        self.id=id
        self.name=name
        self.description=description
        self.price=price
        self.quantity_available=quantity_available
        self.category=category

    def update_quantity(self,new_quantity:int):
        self.quantity_available += new_quantity


        