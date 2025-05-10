class Seat:
    def __init__(self,id,row,column,seat_type):
        self.id = id
        self.row = row 
        self.column = column
        self.seat_type = seat_type  # e.g., Regular, Premium, VIP
    

class SeatStatus:
    AVAILABLE = "available"
    LOCKED = "locked"
    BOOKED = "booked"


class SeatType:
    REGULAR = "regular"
    PREMIUM = "premium"
    VIP = "vip"

