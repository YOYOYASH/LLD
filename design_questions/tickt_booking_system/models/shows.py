from datetime import datetime

from design_questions.bookmyshow import Movie, Screen


class Show:
    def __init__(self, show_id:int, movie:Movie, screen:Screen, start_time: datetime):
        self.show_id = show_id
        self.movie = movie
        self.screen = screen
        self.start_time = start_time
        self.seats_status = {}  # seat_id -> SeatStatus