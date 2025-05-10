from models.seatlock import SeatLock
import threading

class SeatLockService:
    def __init__(self,lock_timeout):
        self.locks = {}  # --> (seat_id,user_id) - > SeatLock
        self.lock_timeout = lock_timeout
        self.lock = threading.Lock()
    

    def lock_seat(self,seat_id,show_id,user_id):
        key  = (show_id,seat_id)
        with self.lock:
            if self.is_seat_locked(show_id,seat_id):
                raise Exception(f"Seat {seat_id} is already locked or booked!!")
            self.locks[key] = SeatLock(seat_id,user_id,self.lock_timeout)

    
    def is_seat_locked(self,show_id,seat_id):
        key = (show_id,seat_id)
        if key not in self.locks:
            return False
        return not self.locks[key].is_lock_expired()
    
    def validate_lock(self, show_id, seat_id, user_id):
        key = (show_id, seat_id)
        if key not in self.locks:
            return False
        return self.locks[key].user_id == user_id and not self.locks[key].is_lock_expired()