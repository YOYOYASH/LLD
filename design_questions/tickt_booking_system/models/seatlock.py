from datetime import datetime,timedelta

class SeatLock:
    def __init__(self,seat_id,user_id,lock_expires_in):
        self.user_id = user_id
        self.seat_id = seat_id
        self.locked_at = datetime.now()
        self.expires_at  =  self.locked_at + timedelta(seconds=lock_expires_in)
        
    def is_lock_expired(self):
        return datetime.now() > self.expires_at