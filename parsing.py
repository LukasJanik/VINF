from os import listdir
import gzip
import json
import re

from models import Artist, Album, Track, TrackContribution, Recording, AwardNomination

file = 'freebase-head-1000000'

# path_to_file = '../data'
# with gzip.GzipFile(file, 'r') as fin:   
#     for line in fin:
#         print(line)
ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
TRACK_CONTRIBUTION = 'track_contribution'
RECORDING = 'recording'
AWARD_NOMINATION = 'award_nomination'

NOMINATION_TYPE_ARTIST = 'nomination_artist'
NOMINATION_TYPE_WORK = 'nomination_work'

ENTITY_CREATION_BY_NAME = {
    'artist': Artist,
    'track': Track,
    'album': Album,
    'track_contribution': TrackContribution,
    'recording': Recording,
    'award_nomination': AwardNomination
}

# ARTIST
# Matching patterns
# PATTERN_ARTIST = r'\<.*\>\s+(\<.*ns#type\>|\<.*type\.object\.type\>)\s+\<.*ns\/music\.artist\>'
PATTERN_ARTIST = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.artist\>|\<.*music\.artist.*\>\s+\<.*\>)'
PATTERN_ARTIST_TRACK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track\>\t+\<.*\>'
PATTERN_ARTIST_TRACK_CONTRIBUTION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track_contributions\>\t+\<.*\>'
PATTERN_ARTIST_ALBUM = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.album\>\t+\<.*\>'
PATTERN_ARTIST_ACTIVE_START = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>.*'
PATTERN_ARTIST_ACTIVE_END = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>.*'
PATTERN_ARTIST_ORIGIN = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.origin\>\t+\<.*\>'
PATTERN_ARTIST_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.genre\>\t+\<.*\>'
PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>.*'
PATTERN_ARTIST_AWARD_NOMINATION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_nominee\.award_nominations\>.*'
PATTERN_ARTIST_AWARDS_WON = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_winner\.awards_won\>.*'
# Value retrieval patterns
PATTERN_RETRIEVE_ARTIST_ACTIVE_DATE = r'(?<!not )((?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>\t\")|(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>\t\"))([0-9-]*)'
PATTERN_RETRIEVE_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>\t\")([0-9-]*)'


# ALBUM
# Matching patterns
PATTERN_ALBUM = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.album\>|\<.*music\.album.*\>\s+\<.*\>)'
PATTERN_ALBUM_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.artist\>\t+\<.*\>'
PATTERN_ALBUM_RELEASE_DATE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.release_date\>.*'
# Value retrieval patterns
PATTERN_RETRIEVE_ALBUM_RELEASE_DATE = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.release_date\>\t\")([0-9-]*)'


# RECORDING
# Matching patterns
PATTERN_RECORDING = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.recording\>|\<.*music\.recording.*\>\s+\<.*\>)'
PATTERN_RECORDING_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.artist\>\t+\<.*\>'
PATTERN_RECORDING_LENGTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.length\>\t+\<.*\>'
# Value retrieval patterns
PATTERN_RETRIEVE_RECORDING_LENGTH = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.length\>\t\")([0-9]*)'


# GENERAL
# Matching patterns
PATTERN_OBJECT_NAME = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t+\".*\"@en'
PATTERN_OBJECT_DESCRIPTION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.topic\.description\>\t+\".*\"@en'
PATTERN_AWARD_NOMINATED_WORK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_nominated_work\.award_nominations\>.*'

# Value retrieval patterns
PATTERN_RETRIEVE_SUBJECT_ID = r'(?<=\<http:\/\/rdf\.freebase\.com\/ns\/)([a-z]\.[a-z0-9_]+)'
PATTERN_RETRIEVE_OBJECT_ID = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/)[a-z]\.[a-z0-9_]+'
PATTERN_RETRIEVE_OBJECT_NAME = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t\")([\sa-zA-z]*)'
PATTERN_RETRIEVE_OBJECT_DESCRIPTION = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/common\.topic\.description\>\t\")([\sa-zA-z]*)'

def getSubjectId(input: str):
    result = re.search(PATTERN_RETRIEVE_SUBJECT_ID, line)
    return result.group(1) 

def getObjectId(input: str):
    result = re.search(PATTERN_RETRIEVE_OBJECT_ID, line)
    return result.group(0) 

def getDate(pattern: any, input: str):
    result = re.search(pattern, line)
    return result.group(0)

def getName(input: str):
    result = re.search(PATTERN_RETRIEVE_OBJECT_NAME, line)
    return result.group(0)

def getDescription(input: str):
    result = re.search(PATTERN_RETRIEVE_OBJECT_DESCRIPTION, line)
    return result.group(0)

def getLength(pattern: any, input: str):
    result = re.search(pattern, line)
    return result.group(0)

def getOrCreate(data: dict, entity: str, id: int):
    entity_instance = None
    if (id not in data[entity]):
        entity_instance = ENTITY_CREATION_BY_NAME[entity](id)
        data[entity][id] = entity_instance
    else:
        entity_instance = data[entity][id]
    return entity_instance, data

def handleArtistParsing(data, line: str):
    _data = data[ARTIST][found_id]
    if (re.match(PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)):
        _data.date_of_birth = getDate(PATTERN_RETRIEVE_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)
    elif (re.match(PATTERN_ARTIST_ACTIVE_START, line)):
        _data.active_start = getDate(PATTERN_RETRIEVE_ARTIST_ACTIVE_DATE,line)
    elif (re.match(PATTERN_ARTIST_ACTIVE_END, line)):
        _data.active_end = getDate(PATTERN_RETRIEVE_ARTIST_ACTIVE_DATE,line)
    elif (re.match(PATTERN_ARTIST_ORIGIN, line)):
        _data.origin = getObjectId(line)
    elif (re.match(PATTERN_ARTIST_GENRE, line)):
        _data.genre = getObjectId(line)
    elif (re.match(PATTERN_OBJECT_NAME, line)):
        _data.name = getName(line)
    elif (re.match(PATTERN_ARTIST_TRACK, line)):
        track, data = getOrCreate(data, TRACK, getObjectId(line))
        _data.tracks.append(track)
    elif (re.match(PATTERN_ARTIST_ALBUM, line)):
        album, data = getOrCreate(data, ALBUM, getObjectId(line))
        _data.albums.append(album)
    elif (re.match(PATTERN_ARTIST_TRACK_CONTRIBUTION, line)):
        track_contribution, data = getOrCreate(data, TRACK_CONTRIBUTION, getObjectId(line))
        _data.track_contributions.append(track_contribution)
    elif (re.match(PATTERN_ARTIST_AWARD_NOMINATION, line)):
        award_nomination, data = getOrCreate(data, AWARD_NOMINATION, getObjectId(line))
        award_nomination.nomination_type = NOMINATION_TYPE_ARTIST
        _data.award_nominations.append(award_nomination)
    elif (re.match(PATTERN_ARTIST_AWARD_NOMINATION, line)):
        award_nomination, data = getOrCreate(data, AWARD_NOMINATION, getObjectId(line))
        award_nomination.nomination_type = NOMINATION_TYPE_ARTIST
        _data.award_nominations.append(award_nomination)
    return data

def handleRecordingParsing(data, line: str):
    _data = data[RECORDING][found_id]
    if (re.match(PATTERN_OBJECT_NAME, line)):
        _data.name = getName(line)
    elif (re.match(PATTERN_RECORDING_ARTIST, line)):
        artist, data = getOrCreate(data, ARTIST, getObjectId(line))
        # artist.tracks.append(_data)
        _data.artists.append(artist)
    elif (re.match(PATTERN_RECORDING_LENGTH, line)):
        _data.length = getLength(PATTERN_RETRIEVE_RECORDING_LENGTH, input)
    elif (re.match(PATTERN_AWARD_NOMINATED_WORK, line)):
        award_nominated_work, data = getOrCreate(data, AWARD_NOMINATION, getObjectId(line))
        award_nominated_work.nomination_type = NOMINATION_TYPE_WORK
        _data.awards_nominated.append(award_nominated_work)
    return data

def handleAlbumParsing(data, line: str):
    _data = data[ALBUM][found_id]
    if (re.match(PATTERN_OBJECT_NAME, line)):
        _data.name = getName(line)
    elif (re.match(PATTERN_OBJECT_DESCRIPTION, line)):
        _data.description = getDescription(line)
    elif (re.match(PATTERN_ALBUM_ARTIST, line)):
        artist, data = getOrCreate(data, ARTIST, getObjectId(line))
        artist.albums.append(_data)
        _data.artists.append(artist)
    elif (re.match(PATTERN_ALBUM_RELEASE_DATE, line)):
        _data.release_date = getLength(PATTERN_RETRIEVE_ALBUM_RELEASE_DATE, input)
    elif (re.match(PATTERN_AWARD_NOMINATED_WORK, line)):
        award_nominated_work, data = getOrCreate(data, AWARD_NOMINATION, getObjectId(line))
        award_nominated_work.nomination_type = NOMINATION_TYPE_WORK
        _data.awards_nominated.append(award_nominated_work)        
    return data

ENTITY_PARSING_BY_NAME = {
    'artist': handleArtistParsing,
    'recording': handleRecordingParsing,
    'album': handleAlbumParsing
}

f = open(file, "r", encoding="utf8")
line = f.readline()

found_id = None
currently_parsing = None
line_counter: int = 0

data = dict()
data[ARTIST] = dict()
data[TRACK] = dict()
data[ALBUM] = dict()
data[TRACK_CONTRIBUTION] = dict()
data[RECORDING] = dict()
data[AWARD_NOMINATION] = dict()

while (line != ''):
    if (currently_parsing == None or (found_id != None and getSubjectId(line) != found_id)):
        # is it artist?
        if (re.match(PATTERN_ARTIST, line)):
            currently_parsing = ARTIST
            found_id = getSubjectId(line)
            artist, data = getOrCreate(data, ARTIST, found_id)
        # is it recording?
        elif(re.match(PATTERN_RECORDING, line)):
            currently_parsing = RECORDING
            found_id = getSubjectId(line)
            recording, data = getOrCreate(data, RECORDING, found_id)
        # is it album?            
        elif(re.match(PATTERN_ALBUM, line)):
            currently_parsing = ALBUM
            found_id = getSubjectId(line)
            album, data = getOrCreate(data, ALBUM, found_id)
        else:
            found_id = None
            currently_parsing = None
    if (currently_parsing != None):
        data = ENTITY_PARSING_BY_NAME[currently_parsing](data, line)

    line_counter += 1
    if (line_counter % 100000 == 0):
        print(line_counter)
    line = f.readline()
print('this is the end')