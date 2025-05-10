from models.booking import Booking
from models.seats import SeatStatus
from services.paymentservice import PaymentService,PaymentServiceFactory
import threading

class BookingService:
    def __init__(self,seat_lock_service):
        self.bookings = []
        self.seat_lock_service = seat_lock_service
        self.lock = threading.Lock()
    
    def create_booking(self,user_id,show,seat_ids,payment_method):
        with self.lock:
            for seat_id in seat_ids:
                if not self.seat_lock_service.validate_lock(show.show_id,seat_id,user_id):
                    raise Exception(f"Seat {seat_id} is not properly locked")
            
            total_cost =  len(seat_ids) * 200
            if  not self.process_payment(total_cost,payment_method):
                raise Exception("Payment failed")
            
            for seat_id in seat_ids:
                show.seats_status[seat_id] = SeatStatus.BOOKED

            booking = Booking(f"B{len(self.bookings)+1}",user_id,show.show_id,seat_ids)
            self.bookings.append(booking)
            return booking
    
    def process_payment(self,amount,payment_type):
        payment_strategy = PaymentServiceFactory.set_strategy(payment_type,{})
        payment_context = PaymentService(payment_strategy)
        return payment_context.execute_payment(amount)
    


        