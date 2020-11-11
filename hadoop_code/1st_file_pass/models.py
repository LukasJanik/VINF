#!/usr/bin/env python
"""models.py"""

from constants import *

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

class Award:
    id = None
    name = None
    description = None
    object_type = None
    detail_object = None

    entity_type = None

    def __init__(self, id):
        self.id = id
        self.name = None
        self.description = None
        self.object_type = None
        self.detail_object = None
        
        self.entity_type = AWARD
    
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