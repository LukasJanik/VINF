from os import listdir
import gzip
import json
import re

from models import Artist, Album, Track

file = 'freebase-head-1000000'

# path_to_file = '../data'
# with gzip.GzipFile(file, 'r') as fin:   
#     for line in fin:
#         print(line)
ARTIST = 'artist'
# Matching patterns
PATTERN_ARTIST = r'\<.*\>\s+(\<.*ns#type\>|\<.*type\.object\.type\>)\s+\<.*ns\/music\.artist\>'
PATTERN_ARTIST_TRACK = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.track\>\t+\<.*\>'
PATTERN_ARTIST_ALBUM = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.album\>\t+\<.*\>'
PATTERN_ARTIST_ACTIVE_START = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>\t+\<.*\>'
PATTERN_ARTIST_ACTIVE_END = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>\t+\<.*\>'
PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>\t+\<.*\>'

# Value retrieval patterns
PATTERN_RETRIEVE_ARTIST_ACTIVE_DATE = r'(?<!not )((?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_end\>\t\")|(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/music\.artist\.active_start\>\t\"))([0-9-]*)'
PATTERN_RETRIEVE_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/people\.person\.date_of_birth\>\t\")([0-9-]*)'

# Value retrieval patterns
PATTERN_SUBJECT_ID = r'(?<=\<http:\/\/rdf\.freebase\.com\/ns\/)(g\.[a-z0-9_]+)'
PATTERN_OBJECT_ID = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/)[a-z]\.[a-z0-9]+'

def getSubjectId(input: str):
    result = re.search(PATTERN_SUBJECT_ID, line)
    return result.group(1) 

def getObjectId(input: str):
    result = re.search(PATTERN_OBJECT_ID, line)
    return result.group(0) 

def getDate(pattern: any, input: str):
    result = re.search(pattern, line)
    return result.group(0) 

f = open(file, "r", encoding="utf8")
line = f.readline()

found_id = None
currently_parsing = None

data = dict()
data['artists'] = dict()
data['tracks'] = dict()
data['albums'] = dict()


while (line != None):
    if (currently_parsing == None or (found_id != None and getSubjectId(line) != found_id)):
        # is it artist?
        if (re.match(PATTERN_ARTIST, line)):
            currently_parsing = ARTIST
            found_id = getSubjectId(line)
            data['artists'][found_id] = Artist(found_id)
        else:
            found_id = None
            currently_parsing = None
    else:
        if (currently_parsing == ARTIST):
            if (re.match(PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)):
                data['artists'][found_id].date_of_birth = getDate(PATTERN_RETRIEVE_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)
            elif (re.match(PATTERN_ARTIST_ACTIVE_START, line) or re.match(PATTERN_ARTIST_ACTIVE_END, line)):
                data['artists'][found_id]['active_start' if re.match(PATTERN_ARTIST_ACTIVE_START, line) else 'active_end'] = getDate(PATTERN_RETRIEVE_ARTIST_ACTIVE_DATE,line)                
            elif (re.match(PATTERN_ARTIST_TRACK, line)):
                track_id = getObjectId(line)
                if (track_id not in data['tracks']):
                    new_track = Track(track_id)
                    data['tracks'][track_id] = new_track
                    data['artists'][found_id].tracks.append(new_track)
            elif (re.match(PATTERN_ARTIST_ALBUM, line)):
                album_id = getObjectId(line)
                if (album_id not in data['albums']):
                    new_album = Album(album_id)
                    data['albums'][album_id] = new_album
                    data['artists'][found_id].albums.append(new_track)
    line = f.readline()