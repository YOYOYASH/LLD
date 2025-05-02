
class Genre:
    SCIFI = "scifi"
    DRAMA = "drama"
    COMEDY = "comedy"
    THRILLER = "thriller"
    HORROR = "horror"
    ACTION = "action"


class Movie:
    def __init__(self,id:str,title:str,description:str,genre:Genre,duration_in_minutes:int):
        self.id = id
        self.title = title
        self.description  =description
        self.genre = genre
        self.duration_in_minutes   = duration_in_minutes






        