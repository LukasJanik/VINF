#!/usr/bin/env python
"""mapper.py"""

import sys
import re
import jsonpickle
import json
import os


ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
GENRE = 'genre'
AWARD = 'award'
AWARD_INFO_TYPE_AWARD_WON = 'award_won'


# ARTIST
PATTERN_ARTIST = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.artist\>|\<.*music\.artist.*\>\s+\<.*\>)'
PATTERN_ARTIST_TRACK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_ALBUM = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.album\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_ACTIVE_START = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>\t+\"(?P<date>[0-9-]*)\"'
PATTERN_ARTIST_ACTIVE_END = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>\t+\"(?P<date>[0-9-]*)\"'
PATTERN_ARTIST_ORIGIN = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.origin\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.genre\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>\t+\"(?P<date>[0-9-]*)\"'
PATTERN_ARTIST_AWARDS_WON = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_winner\.awards_won\>\t+\<.*\/(?P<object_id>[gm].*)\>'

# ALBUM
PATTERN_ALBUM = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.album\>|\<.*music\.album.*\>\s+\<.*\>)'
PATTERN_ALBUM_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.artist\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ALBUM_RELEASE_DATE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.release_date\>\t+\"(?P<date>[0-9-]*)\"'

# AWARD
PATTERN_AWARD_HONOR_AWARD = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_honor\.award\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_AWARD_HONOR_AWARD_WINNER = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_honor\.award_winner\>\t+\<.*\/(?P<object_id>[gm].*)\>'

# RECORDING
PATTERN_RECORDING = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.recording\>|\<.*music\.recording.*\>\s+\<.*\>)'
PATTERN_RECORDING_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.artist\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_RECORDING_LENGTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.length\>\t+(?P<length>[0-9]*)'

# GENRE
PATTERN_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.predicate\>\t+\"\/music\/(?P<type>artist|album)\/genre\"'
PATTERN_GENRE_NAME = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.display_name\>\t+\"(?P<name>.*)\"@en'

# GENERAL
# Matching patterns
PATTERN_OBJECT_NAME = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t+\"(?P<name>.*)\"@en'
PATTERN_OBJECT_DESCRIPTION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.topic\.description\>\t+\"(?P<description>.*)\"@en'
# PATTERN_AWARD_NOMINATED_WORK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_nominated_work\.award_nominations\>.*'

# Value retrieval patterns
PATTERN_RETRIEVE_SUBJECT_ID = r'(?<=\<http:\/\/rdf\.freebase\.com\/ns\/)([a-z]\.[a-z0-9_]+)\>\t\<'
PATTERN_RETRIEVE_OBJECT_ID = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/)[a-z]\.[a-z0-9_]+'

sys.path.append('.')

class Album:
    id = None
    name = None
    description = None            

    artists = []                
    release_date = None           
    entity_type = None

    def __init__(self, id):
        self.id = id
        self.name = None
        self.description = None
        self.release_date = None
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

class Track:
    id = None
    name = ''
    description = ''
    artists = []
    tracks = []               
    length = None             
    entity_type = ''

    def __init__(self, id):
        self.id = id
        self.name = None
        self.description = None
        self.artists = []
        self.tracks = []
        self.length = None
        self.entity_type = TRACK

def getOrCreate(data, entity, id):
    entity_instance = None
    if (id not in data):
        entity_instance = ENTITY_CREATION_BY_NAME[entity](id)
        entity_instance.entity_type = entity
        data[id] = entity_instance
    else:
        entity_instance = data[id]
    return entity_instance, data

def getSubjectId(input):
    result = re.search(PATTERN_RETRIEVE_SUBJECT_ID, input)
    return None if result == None else result.group(1) 

def getObjectId(input):
    result = re.search(PATTERN_RETRIEVE_OBJECT_ID, input)
    return None if result == None else result.group(0) 

def handleCommon(data, line):
    if (re.match(PATTERN_OBJECT_NAME, line)):
        match = re.match(PATTERN_OBJECT_NAME, line)
        data.name = match.group('name')
    elif (re.match(PATTERN_OBJECT_DESCRIPTION, line)):
        match = re.match(PATTERN_OBJECT_DESCRIPTION, line)
        data.description = match.group('description')  
    return data

def handleArtistParsing(data, line, found_id):
    _data = data[found_id]
    _data = handleCommon(_data, line)
    if (re.match(PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)):
        match = re.match(PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)
        _data.date_of_birth = match.group('date')
    elif (re.match(PATTERN_ARTIST_ACTIVE_START, line)):
        match = re.match(PATTERN_ARTIST_ACTIVE_START, line)
        _data.active_start = match.group('date')
    elif (re.match(PATTERN_ARTIST_ACTIVE_END, line)):
        match = re.match(PATTERN_ARTIST_ACTIVE_END, line)
        _data.active_end = match.group('date')
    elif (re.match(PATTERN_ARTIST_ORIGIN, line)):
        match = re.match(PATTERN_ARTIST_ORIGIN, line)
        _data.origin = match.group('object_id')
    elif (re.match(PATTERN_ARTIST_GENRE, line)):
        match = re.match(PATTERN_ARTIST_GENRE, line)
        _data.genre = match.group('object_id')
    elif (re.match(PATTERN_ARTIST_TRACK, line)):
        match = re.match(PATTERN_ARTIST_TRACK, line)
        _data.tracks.append(match.group('object_id'))
    elif (re.match(PATTERN_ARTIST_ALBUM, line)):
        match = re.match(PATTERN_ARTIST_ALBUM, line)
        _data.albums.append(match.group('object_id'))
    elif (re.match(PATTERN_ARTIST_AWARDS_WON, line)):
        match = re.match(PATTERN_ARTIST_AWARDS_WON, line)
        object_id = match.group('object_id')
        award_won, data = getOrCreate(data, AWARD, object_id)
        award_won.object_type = AWARD_INFO_TYPE_AWARD_WON
        printObject(object_id, award_won)
        _data.awards_won.append(award_won.id)
    return data

def handleTrackParsing(data, line, found_id):
    _data = data[found_id]
    _data = handleCommon(_data, line) 
    if (re.match(PATTERN_RECORDING_ARTIST, line)):
        match = re.match(PATTERN_RECORDING_ARTIST, line)
        _data.artists.append(match.group('object_id'))
    elif (re.match(PATTERN_RECORDING_LENGTH, line)):
        match = re.match(PATTERN_RECORDING_LENGTH, line)
        _data.length = match.group('length')
    return data

def handleAlbumParsing(data, line, found_id):
    _data = data[found_id]
    _data = handleCommon(_data, line)
    if (re.match(PATTERN_ALBUM_ARTIST, line)):
        match = re.match(PATTERN_ALBUM_ARTIST, line)
        # data[match.group('object_id')].albums.append(found_id)
        _data.artists.append(match.group('object_id'))
    elif (re.match(PATTERN_ALBUM_RELEASE_DATE, line)):
        match = re.match(PATTERN_ALBUM_RELEASE_DATE, line)
        _data.release_date = match.group('date')    
    return data

def handleGenreParsing(data, line, found_id):
    _data = data[found_id]
    if (re.match(PATTERN_GENRE, line)):
        _data.genre_type = re.match(PATTERN_GENRE, line).group('type')
    if (re.match(PATTERN_GENRE_NAME, line)):
        match = re.match(PATTERN_GENRE_NAME, line)
        _data.name = match.group('name')
    if (re.match(PATTERN_GENRE, line)):
        _data.genre_type = re.match(PATTERN_GENRE, line).group('type')
    return data

ENTITY_PARSING_BY_NAME = {
    'artist': handleArtistParsing,
    'track': handleTrackParsing,
    'album': handleAlbumParsing
}

ENTITY_CREATION_BY_NAME = {
    'artist': Artist,
    'track': Track,
    'album': Album,
    'award': Award,
    'genre': Genre
}

def printObject(id, _object):
    jsonData = jsonpickle.encode(_object, unpicklable=False)
    print(str(id) + '\t' + str(jsonData))

def readIdsAndTypes(fileName):
    onlyIdsAndTypes = dict()
    # f = open('./2nd_file_pass/' + fileName, "r", encoding="utf8")
    # f = open(fileName, "r", encoding="utf8")
    f = open(fileName, "r")
    line = f.readline()
    while line != '':
        curr_id, curr_entity_type = line.rstrip().split('\t', 1)
        onlyIdsAndTypes[curr_id] = curr_entity_type
        line = f.readline()
    f.close()
    return onlyIdsAndTypes

# fileName = 'file.txt'
fileName = 'input_100M'
data = dict()
onlyIdsAndTypes = readIdsAndTypes(fileName)

previous_id = None

for line in sys.stdin:
    found_id = getSubjectId(line)
    if (found_id != None and found_id in onlyIdsAndTypes):
        entity_type = onlyIdsAndTypes[found_id]
        if found_id not in data:
            entity, data = getOrCreate(data, entity_type, found_id)

        if (entity_type == ARTIST):
            data = handleArtistParsing(data, line, found_id)
        elif (entity_type == ALBUM):
            data = handleAlbumParsing(data, line, found_id)
        elif (entity_type == TRACK):
            data = handleTrackParsing(data, line, found_id)
        elif (entity_type == GENRE):
            data = handleGenreParsing(data, line, found_id)
        elif (re.match(PATTERN_AWARD_HONOR_AWARD_WINNER, line)):
            object_id = getObjectId(line)
            if (object_id in onlyIdsAndTypes and onlyIdsAndTypes[object_id] == ARTIST): 
                award, data = getOrCreate(data, AWARD, found_id)
                data[object_id].awards_won.append(found_id)
                printObject(found_id, award)
                # data[object_id].awards_won.append(entity_instance.id)
        if (previous_id == None or (previous_id != None and previous_id != found_id)):
            if (previous_id != None):
                printObject(previous_id, data[previous_id])
            previous_id = found_id
