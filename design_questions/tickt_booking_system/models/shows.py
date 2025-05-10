from datetime import datetime
from models.movies import Movie
from models.screens import Screen



class Show:
    def __init__(self, show_id:int, movie:Movie, screen:Screen, start_time: datetime):
        self.show_id = show_id
        self.movie = movie
        self.screen = screen
        self.start_time = start_time
        self.seats_status = {}  # seat_id -> SeatStatus