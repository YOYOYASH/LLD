from datetime import datetime, timedelta
from threading import Thread
from models.movies import Movie, Genre
from models.screens import Screen
from models.theatre import Theater
from models.shows import Show
from models.seats import SeatStatus,Seat,SeatType
from services.bookingService import BookingService
from services.seatlockservice import SeatLockService


def try_booking(user_id, seat_id, payment_type):
    try:
        seat_lock_service.lock_seat(seat_id,show.show_id, user_id)
        booking = booking_service.create_booking(user_id, show, [seat_id], payment_type)
        print(f"✅ Booking Confirmed: {booking.booking_id} for seats: {', '.join(booking.seats)} for user "
          f"{booking.user_id} at show {booking.show}. "
          f"✅ Payment method: upi")
    except Exception as e:
        print(f"❌ {user_id} failed: {e}")


if __name__ == '__main__':
    movie = Movie(id="M1", title="Inception",language='English',genre=Genre.SCIFI,duration_in_minutes='150')
    screen = Screen(screen_id="S1", name="Screen 1", seat_layout=[Seat("A1",row=1,column='J',seat_type=SeatType.REGULAR), Seat("A2",row=10,column='M',seat_type=SeatType.VIP)])
    theater = Theater(theater_id="T1", name="INOX", city="Delhi")
    theater.add_screen(screen)
    show = Show(show_id="SH1", movie=movie, screen=screen, start_time= datetime.now() + timedelta(seconds=3600))

    #Intially all seats are empty``
    show.seats_status = {seat.id: SeatStatus.AVAILABLE for seat in screen.seats}

    #Seat lock service
    seat_lock_service =SeatLockService(60)
    booking_service = BookingService(seat_lock_service)


    # seat_lock_service.lock_seat(show_id="SH1", seat_id="A1", user_id="U1")
    # seat_lock_service.lock_seat(show_id="SH1", seat_id="A2", user_id="U1")

    # #Create booking after user confirms payment

    # booking = booking_service.create_booking(
    # user_id="U1",
    # show=show,
    # seat_ids=["A1", "A2"],
    # payment_method="upi"
    # )

    t1 = Thread(target=try_booking, args=("U1", "A1", "upi"))
    t2 = Thread(target=try_booking, args=("U2", "A1", "cash"))

    t1.start()
    t2.start()
    t1.join()
    t2.join()


    