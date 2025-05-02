from datetime import datetime, timedelta

#--------------------SeastLOckService-----------

class SeatLock:
    def __init__(self,seat_id,user_id,lock_expires_in):
        self.user_id = user_id
        self.seat_id = seat_id
        self.locked_at = datetime.now()
        self.expires_at  =  self.locked_at + timedelta(seconds=lock_expires_in)
        
    def is_lock_expired(self):
        return datetime.now() > self.expires_at


class SeatLockService:
    def __init__(self,lock_timeout):
        self.locks = {}  # --> (seat_id,user_id) - > SeatLock
        self.lock_timeout = lock_timeout
    
    def lock_seat(self,seat_id,show_id,user_id):
        key  = (show_id,seat_id)
        if self.is_seat_locked(show_id,seat_id):
           raise Exception("Seat is already locked or booked!!")
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

#-----------------------------------BookingService-------------------------------

class Booking:
    def __init__(self,id,user_id,show,seats):
        self.booking_id = id
        self.user_id = user_id
        self.show = show
        self.seats = seats
    
class BookingService:
    def __init__(self,seat_lock_service):
        self.bookings = []
        self.seat_lock_service = seat_lock_service
    
    def create_booking(self,user_id,show,seat_ids):
        for seat_id in seat_ids:
            if not self.seat_lock_service.validate_lock(show.show_id,seat_id,user_id):
                raise Exception(f"Seat {seat_id} not lockeed properly.")
        
        for seat_id in seat_ids:
            show.seats_status[seat_id] = SeatStatus.BOOKED
        
        booking = Booking(f"BK-{len(self.bookings)+1}", user_id, show, seat_ids)
        self.bookings.append(booking)
        return booking


class Movie:
    def __init__(self, movie_id, title, language, duration_mins, genre):
        self.movie_id = movie_id
        self.title = title
        self.language = language
        self.duration_mins = duration_mins
        self.genre = genre

class Screen:
    def __init__(self, screen_id, name, seat_layout):
        self.screen_id = screen_id
        self.name = name
        self.seats = seat_layout  # 2D or 1D array of Seat objects


class Theater:
    def __init__(self, theater_id, name, city):
        self.theater_id = theater_id
        self.name = name
        self.city = city
        self.screens = []  # List of Screen objects

    def add_screen(self, screen):
        self.screens.append(screen)
    


class Show:
    def __init__(self, show_id, movie, screen, start_time: datetime):
        self.show_id = show_id
        self.movie = movie
        self.screen = screen
        self.start_time = start_time
        self.seats_status = {}  # seat_id -> SeatStatus


class Seat:
    def __init__(self, seat_id, row, number):
        self.seat_id = seat_id
        self.row = row
        self.number = number


class SeatStatus:
    AVAILABLE = "available"
    LOCKED = "locked"
    BOOKED = "booked"


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name


if __name__ == '__main__':
    movie = Movie(movie_id="M1", title="Inception",language='English',duration_mins='150',genre='Sci-Fi')
    screen = Screen(screen_id="S1", name="Screen 1", seat_layout=[Seat("A1",row=1,number=7), Seat("A2",row=2,number=5)])
    theater = Theater(theater_id="T1", name="INOX", city="Delhi")
    theater.add_screen(screen)
    show = Show(show_id="SH1", movie=movie, screen=screen, start_time= datetime.now() + timedelta(seconds=3600))

    #Intially all seats are empty
    show.seats_status = {seat.seat_id: SeatStatus.AVAILABLE for seat in screen.seats}

    #Seat lock service
    seat_lock_service =SeatLockService(60)
    booking_service = BookingService(seat_lock_service)


    seat_lock_service.lock_seat(show_id="SH1", seat_id="A1", user_id="U1")
    seat_lock_service.lock_seat(show_id="SH1", seat_id="A2", user_id="U1")

    #Create booking after user confirms payment

    booking = booking_service.create_booking(
    user_id="U1",
    show=show,
    seat_ids=["A1", "A2"]
    )
    print(f"✅ Booking Confirmed: {booking.booking_id}")