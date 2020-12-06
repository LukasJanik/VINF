def processDescription(description:str) -> str:
    return description.replace('\n', '').replace('\"', '"') if description != None else None

def transformDate(date:str) -> str:
    if date == None:
        return None

    date_parts = date.strip().split('-')
    
    no_of_parts = len(date_parts)

    if no_of_parts == 3:
        return date
    if no_of_parts == 2:
        return f"{date}-01"
    else:
        return f"{date}-01-01"

class Track:
    name: str
    description: str          

    def __init__(self, id:str, name:str, description:str):
        self.id = id
        self.name = name
        self.description = processDescription(description)
    
class Album:
    name: str
    description: str        
    release_date: int       

    def __init__(self, id:str, name:str, description:str, release_date:str):
        self.id = id
        self.name = name
        self.description = processDescription(description)
        self.release_date = transformDate(release_date)

class Artist:
    name: str
    description: str
    active_start: str
    active_end: str  
    date_of_birth: str

    tracks: []                  
    albums: []                  
    awards_won: []

    no_of_tracks = 0
    no_of_albums = 0
    no_of_awards_won = 0              

    def __init__(self, id:str, name:str, description:str, active_start:str, active_end:str, date_of_birth:str):
        self.id = id
        self.name = name
        self.description = processDescription(description)
        self.active_start = transformDate(active_start)
        self.active_end = transformDate(active_end)
        self.date_of_birth = transformDate(date_of_birth)

        self.tracks = []
        self.albums = []
        self.awards_won = []

        self.no_of_tracks = 0
        self.no_of_albums = 0
        self.no_of_awards_won = 0 
        

class Award:
    id: int
    name: str
    description: str

    def __init__(self, id:str, name:str, description:str):
        self.id = id
        self.name = name
        self.description = processDescription(description)