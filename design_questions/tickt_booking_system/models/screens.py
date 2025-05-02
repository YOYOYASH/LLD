class Screen:
    def __init__(self, screen_id, name, seat_layout):
        self.screen_id = screen_id
        self.name = name
        self.seats = seat_layout  # 2D or 1D array of Seat objects

