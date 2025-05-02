from abc import ABC, abstractmethod

#Interface
class PaymentService(ABC):
    @abstractmethod
    def complete_payment(self,amount:float):
        pass


#Concerte implementation 
class CreditCardService(PaymentService):
    def __init__(self,card_number:str):
        self.card_number = card_number
    
    def complete_payment(self, amount:float):
        return f"Received payment of {amount} for card number ending with {self.card_number[-4:]}"

class PayPalService(PaymentService):
    def __init__(self,email:str):
        self.email = email
    
    def complete_payment(self, amount:float):
        return f"Recieved payment of {amount} for id: {self.email}"

class UPIService(PaymentService):
    def __init__(self,upi_id:str):
        self.upi_id  =upi_id
    
    def complete_payment(self, amount:float):
        return f"Recieved payment of {amount} for upi id: {self.upi_id}"


#Factory Class
class PaymentServiceFactory:
    @staticmethod
    def set_service(payment_type:str,config:dict):
        if payment_type == 'credit card':
            return CreditCardService(config['card_number'])
        elif payment_type == 'paypal':
            return PayPalService(config['email'])
        elif payment_type == 'upi':
            return UPIService(config['upi_id'])
        else:
            raise ValueError("Payment type not supported!")
    
if __name__ == '__main__':
    payment_type = input("Enter payment type: ").strip().lower()
    amount = float(input("Enter amount in format XXX.YY: ").strip())
    config = {
        "email": "user@example.com",
        "card_number": "1234567890123456",
        "upi_id": "user@upi"
    }
    payment_service = PaymentServiceFactory.set_service(payment_type,config)
    print(payment_service.complete_payment(amount))