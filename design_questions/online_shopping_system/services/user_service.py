from models.user import User
import uuid

class UserService:
    def __init__(self):
        self.users = {} # id -> user

    def register_user(self,name:str,email:str):
        user_id = str(uuid.uuid4())
        new_user = User(user_id,name,email)
        self.users[user_id] = new_user
        return new_user

    def remove_user(self,user_id:str):
        if user_id in self.users:
            del self.users[user_id]
    
    
               