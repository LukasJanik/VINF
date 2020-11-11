#!/usr/bin/env python
"""mapper.py"""

import sys
import re
import jsonpickle
import json

# from patterns import *
# from constants import *
# from models import *

class Track:
    id = None
    name = ''
    description = ''
    artists = []
    tracks = []               
    length = None             
    awards_won = []       
    awards_nominated = []

    entity_type = ''

    def __init__(self, id):
        self.id = id
        self.name = None
        self.description = None
        self.artists = []
        self.tracks = []
        self.length = None

        self.awards_won = []
        self.awards_nominated = []

        self.entity_type = TRACK
    
class Album:
    id = None
    name = None
    description = None            

    artists = []                
    release_date = None           
    release_type = None           
    awards_nominated = []
    entity_type = None

    def __init__(self, id):
        self.id = id
        self.name = None
        self.description = None

        self.artists = []
        self.awards_nominated = []

        self.entity_type = ALBUM

class Artist:
    id = None
    name = None                   
    description = None
    active_start = None           
    active_end = None             
    origin = None                 
    genre = None                  
    date_of_birth = None          

    tracks = []                  
    albums = []                  
    # track_contributions = []     
    # award_nominations = []       
    awards_won = []              

    entity_type = None

    def __init__(self, id):
        self.id = id
        self.name = None
        self.description = None
        self.active_start = None
        self.active_end = None
        self.origin = None
        self.genre = None
        self.date_of_birth = None
        
        self.tracks = []
        self.albums = []
        # self.track_contributions = []
        # self.award_nominations = []
        # self.music_group_members = []
        self.awards_won = []

        self.entity_type = ARTIST
   
class Genre:
    id = None
    name = None                   
    genre_type = None             
    entity_type = None
    def __init__(self, id):
        self.id = id
        self.name = None 
        self.genre_type = None 
        self.entity_type = GENRE

PATTERN_RETRIEVE_SUBJECT_ID = r'(?<=\<http:\/\/rdf\.freebase\.com\/ns\/)([a-z]\.[a-z0-9_]+)\>\t\<'
PATTERN_RETRIEVE_OBJECT_ID = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/)[a-z]\.[a-z0-9_]+'

PATTERN_ARTIST = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.artist\>|\<.*music\.artist.*\>\s+\<.*\>)'
PATTERN_ALBUM = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.album\>|\<.*music\.album.*\>\s+\<.*\>)'
PATTERN_RECORDING = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.recording\>|\<.*music\.recording.*\>\s+\<.*\>)'
PATTERN_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.predicate\>\t+\"\/music\/(?P<type>artist|album)\/genre\"'


sys.path.append('.')


ENTITY_CREATION_BY_NAME = {
    'artist': Artist,
    'track': Track,
    'album': Album,
    'genre': Genre
}

ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
GENRE = 'genre'

def getObjectId(input):
    result = re.search(PATTERN_RETRIEVE_OBJECT_ID, input)
    return None if result == None else result.group(0) 

data = set()

for line in sys.stdin:
    object_type = None

    if (re.match(PATTERN_ARTIST, line)):
        object_type = ARTIST
    elif (re.match(PATTERN_RECORDING, line)):
        object_type = TRACK
    elif (re.match(PATTERN_ALBUM, line)):
        object_type = ALBUM
    elif (re.match(PATTERN_GENRE, line)):
        object_type = GENRE

    if (object_type != None):    
        id = getObjectId(line)
        if (id not in data):
            entity_instance = ENTITY_CREATION_BY_NAME[object_type](id)
            data.add(id)
            if (object_type == GENRE):
                entity_instance.genre_type = re.match(PATTERN_GENRE, line).group('type')
            jsonData = jsonpickle.encode(entity_instance, unpicklable=False)
            print(str(id) + "\t" + str(jsonData))
