from os import listdir, system
import gzip
import json
import re

from models import Artist, Album, Track, TrackContribution

file = 'freebase-head-1000000'

clear = lambda: system('cls')

# path_to_file = '../data'
# with gzip.GzipFile(file, 'r') as fin:   
#     for line in fin:
#         print(line)
ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
TRACK_CONTRIBUTION = 'track_contribution'

ENTITY_CREATION_BY_NAME = {
    'artist': Artist,
    'track': Track,
    'album': Album,
    'track_contribution': TrackContribution
}

# Matching patterns
# PATTERN_ARTIST = r'\<.*\>\s+(\<.*ns#type\>|\<.*type\.object\.type\>)\s+\<.*ns\/music\.artist\>'
PATTERN_ARTIST = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.artist\>|\<.*music\.artist.*\>\s+\<.*\>)'
PATTERN_ARTIST_TRACK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track\>\t+\<.*\>'
PATTERN_ARTIST_TRACK_CONTRIBUTION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track_contributions\>\t+\<.*\>'
PATTERN_ARTIST_ALBUM = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.album\>\t+\<.*\>'
PATTERN_ARTIST_ACTIVE_START = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>\t+\<.*\>'
PATTERN_ARTIST_ACTIVE_END = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>\t+\<.*\>'
PATTERN_ARTIST_ORIGIN = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.origin\>\t+\<.*\>'
PATTERN_ARTIST_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.genre\>\t+\<.*\>'
PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>\t+\<.*\>'
PATTERN_ARTIST_NAME = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t+\".*\"@en'

# Value retrieval patterns
PATTERN_RETRIEVE_ARTIST_ACTIVE_DATE = r'(?<!not )((?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>\t\")|(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>\t\"))([0-9-]*)'
PATTERN_RETRIEVE_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>\t\")([0-9-]*)'
PATTERN_RETRIEVE_ARTIST_NAME = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t\")([\sa-zA-z]*)'

# Value retrieval patterns
PATTERN_SUBJECT_ID = r'(?<=\<http:\/\/rdf\.freebase\.com\/ns\/)([a-z]\.[a-z0-9_]+)'
PATTERN_OBJECT_ID = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/)[a-z]\.[a-z0-9_]+'

def getSubjectId(input: str):
    result = re.search(PATTERN_SUBJECT_ID, line)
    return result.group(1) 

def getObjectId(input: str):
    result = re.search(PATTERN_OBJECT_ID, line)
    return result.group(0) 

def getDate(pattern: any, input: str):
    result = re.search(pattern, line)
    return result.group(0)

def getName(input: str):
    result = re.search(PATTERN_RETRIEVE_ARTIST_NAME, line)
    return result.group(0)

def getOrCreate(data: dict, entity: str, id: int):
    entity_instance = None
    if (id not in data[entity]):
        entity_instance = ENTITY_CREATION_BY_NAME[entity](id)
        data[entity][id] = entity_instance
    else:
        entity_instance = data[entity][id]
    return entity_instance, data

f = open(file, "r", encoding="utf8")
line = f.readline()

found_id = None
currently_parsing = None
line_counter: int = 0

data = dict()
data['artist'] = dict()
data['track'] = dict()
data['album'] = dict()
data['track_contribution'] = dict()

data['recording'] = dict()

def handleArtistParsing(data, line: str):
    if (re.match(PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)):
        data['artist'][found_id].date_of_birth = getDate(PATTERN_RETRIEVE_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)
    elif (re.match(PATTERN_ARTIST_ACTIVE_START, line) or re.match(PATTERN_ARTIST_ACTIVE_END, line)):
        data['artist'][found_id]['active_start' if re.match(PATTERN_ARTIST_ACTIVE_START, line) else 'active_end'] = getDate(PATTERN_RETRIEVE_ARTIST_ACTIVE_DATE,line)                
    elif (re.match(PATTERN_ARTIST_ORIGIN, line)):
        data['artist'][found_id].origin = getObjectId(line)
    elif (re.match(PATTERN_ARTIST_GENRE, line)):
        data['artist'][found_id].genre = getObjectId(line)
    elif (re.match(PATTERN_ARTIST_NAME, line)):
        data['artist'][found_id].name = getName(line)
    elif (re.match(PATTERN_ARTIST_TRACK, line)):
        track_id = getObjectId(line)
        track, data = getOrCreate(data, TRACK, track_id)
        data['artist'][found_id].tracks.append(track)
    elif (re.match(PATTERN_ARTIST_ALBUM, line)):
        album_id = getObjectId(line)
        album, data = getOrCreate(data, ALBUM, album_id)
        data['artist'][found_id].albums.append(album)
    elif (re.match(PATTERN_ARTIST_ALBUM, line)):
        album_id = getObjectId(line)
        album, data = getOrCreate(data, ALBUM, album_id)
        data['artist'][found_id].albums.append(album)
    elif (re.match(PATTERN_ARTIST_TRACK_CONTRIBUTION, line)):
        contribution_id = getObjectId(line)
        track_contribution, data = getOrCreate(data, TRACK_CONTRIBUTION, contribution_id)
        data['artist'][found_id].track_contributions.append(track_contribution)
    return data


ENTITY_PARSING_BY_NAME = {
    'artist': handleArtistParsing,
}



while (line != None):
    if (currently_parsing == None or (found_id != None and getSubjectId(line) != found_id)):
        # is it artist?
        if (re.match(PATTERN_ARTIST, line)):
            currently_parsing = ARTIST
            found_id = getSubjectId(line)
            artist, data = getOrCreate(data, ARTIST, found_id)
        else:
            found_id = None
            currently_parsing = None
    if (currently_parsing != None):
        data = ENTITY_PARSING_BY_NAME[currently_parsing](data, line)
    # if (currently_parsing == ARTIST):
    #     data = handleArtistParsing(data, line)
        # if (re.match(PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)):
        #     data['artist'][found_id].date_of_birth = getDate(PATTERN_RETRIEVE_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)
        # elif (re.match(PATTERN_ARTIST_ACTIVE_START, line) or re.match(PATTERN_ARTIST_ACTIVE_END, line)):
        #     data['artist'][found_id]['active_start' if re.match(PATTERN_ARTIST_ACTIVE_START, line) else 'active_end'] = getDate(PATTERN_RETRIEVE_ARTIST_ACTIVE_DATE,line)                
        # elif (re.match(PATTERN_ARTIST_ORIGIN, line)):
        #     data['artist'][found_id].origin = getObjectId(line)
        # elif (re.match(PATTERN_ARTIST_GENRE, line)):
        #     data['artist'][found_id].genre = getObjectId(line)
        # elif (re.match(PATTERN_ARTIST_NAME, line)):
        #     data['artist'][found_id].name = getName(line)
        # elif (re.match(PATTERN_ARTIST_TRACK, line)):
        #     track_id = getObjectId(line)
        #     track, data = getOrCreate(data, TRACK, track_id)
        #     data['artist'][found_id].tracks.append(track)
        # elif (re.match(PATTERN_ARTIST_ALBUM, line)):
        #     album_id = getObjectId(line)
        #     album, data = getOrCreate(data, ALBUM, album_id)
        #     data['artist'][found_id].albums.append(album)
        # elif (re.match(PATTERN_ARTIST_ALBUM, line)):
        #     album_id = getObjectId(line)
        #     album, data = getOrCreate(data, ALBUM, album_id)
        #     data['artist'][found_id].albums.append(album)
        # elif (re.match(PATTERN_ARTIST_TRACK_CONTRIBUTION, line)):
        #     contribution_id = getObjectId(line)
        #     track_contribution, data = getOrCreate(data, TRACK_CONTRIBUTION, contribution_id)
        #     data['artist'][found_id].track_contributions.append(track_contribution)
    if (line_counter % 100000 == 0):
        clear()
    line = f.readline()
    line_counter += 1
    print(line_counter)