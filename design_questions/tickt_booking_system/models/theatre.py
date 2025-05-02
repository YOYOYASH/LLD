class Theater:
    def __init__(self, theater_id, name, city):
        self.theater_id = theater_id
        self.name = name
        self.city = city
        self.screens = []  # List of Screen objects

    def add_screen(self, screen):
        self.screens.append(screen)