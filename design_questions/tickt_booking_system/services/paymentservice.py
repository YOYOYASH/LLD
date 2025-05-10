from abc import ABC, abstractmethod

#Interface
class PaymentStrategy(ABC):
    @abstractmethod
    def complete_payment(self,amount:float):
        pass


#Concerte implementation 
class CreditCardStrategy(PaymentStrategy):
    def __init__(self):
        self.card_number = ""
    
    def set_card_number(self):
        card_number = input("Enter card number: ").strip().lower()
        self.card_number = card_number
    
    def complete_payment(self, amount:float):
        self.set_card_number()
        if self.card_number == 0:
            raise Exception("Card number not set")
        print(f"Received payment of {amount} for card number ending with {self.card_number[-4:]}")
        return True

class CashStrategy(PaymentStrategy):
    
    def complete_payment(self, amount:float):
        print(f"Recieved payment of {amount}")
        return True

class UPIStrategy(PaymentStrategy):
    def __init__(self):
        self.upi_id = ""
    
    def set_upi_id(self):
        upi_id = input("Enter upi id: ").strip().lower()
        self.upi_id = upi_id
    

    def complete_payment(self, amount:float):
        self.set_upi_id()
        if self.upi_id == "":
            raise Exception("UPI ID not set")
        print(f"Recieved payment of {amount} for upi id: {self.upi_id}")
        return True


#Factory Class
class PaymentServiceFactory:
    @staticmethod
    def set_strategy(payment_type:str,config:dict):
        if payment_type == 'credit card':
            return CreditCardStrategy()
        elif payment_type == 'cash':
            return CashStrategy()
        elif payment_type == 'upi':
            return UPIStrategy()
        else:
            raise ValueError("Payment type not supported!")


#Strategy Class:
class PaymentService:
    def __init__(self,strategy:PaymentStrategy):
        self._strategy:PaymentStrategy = strategy

    
    def execute_payment(self,amount:float):
        return self._strategy.complete_payment(amount)