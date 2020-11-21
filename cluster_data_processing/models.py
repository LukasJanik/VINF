class Track:
    name: str
    description: str
    length = int                

    def __init__(self, id:int, name:str, description:str, length:int):
        self.id = id
        self.name = name
        self.description = description
        self.length = length if length != '' else None
    
class Album:
    name: str
    description: str        

    release_date: str       

    def __init__(self, id:int, name:str, description:str, release_date:str):
        self.id = id
        self.name = name
        self.description = description
        self.release_date = release_date

class Artist:
    name: str
    description: str
    active_start: str
    active_end: str  
    date_of_birth: str

    tracks: []                  
    albums: []                  
    awards_won: []              

    def __init__(self, name:str, description:str, active_start:str, active_end:str, date_of_birth:str):
        self.id = id
        self.name = name
        self.description = description
        self.active_start = active_start
        self.active_end = active_end
        self.date_of_birth = date_of_birth

        self.tracks = []
        self.albums = []
        self.awards_won = []

class Award:
    id: int
    name: str
    description: str

    def __init__(self, id: int, name:str, description:str):
        self.id = id
        self.name = name
        self.description = description
    
# class Genre:
#     id: int
#     name: str                 
#     genre_type: str         
    
#     def __init__(self, id:int, name:str, genre_type:str):
#         self.id = id
#         self.name = name 
#         self.genre_type = genre_type 