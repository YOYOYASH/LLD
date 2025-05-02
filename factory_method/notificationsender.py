from abc import ABC, abstractmethod

#Interface
class NotificationSender(ABC):
    @abstractmethod
    def sendNotification(self,message:str):
        pass


#Concrete implementation of interface
class SmSSender(NotificationSender):
    def sendNotification(self, message:str):
        return f"Sending SMS : {message}"
    
class EmailSender(NotificationSender):
    def sendNotification(self, message:str):
        return f"Sending email: {message}"


#factory class
class NotificationService:
    @staticmethod
    def get_type(type:str):
        if type == 'email':
            return EmailSender()
        if type == 'sms':
            return SmSSender()
        else:
            raise ValueError("Invalid notification type")
    

if __name__ == '__main__':
    user_input = input("Enter notification type:").strip().lower()
    sender = NotificationService.get_type(user_input)
    print(sender.sendNotification("Test notification"))