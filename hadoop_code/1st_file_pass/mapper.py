#!/usr/bin/env python
"""mapper.py"""

import sys
import re
import jsonpickle
import json

PATTERN_RETRIEVE_SUBJECT_ID = r'(?<=\<http:\/\/rdf\.freebase\.com\/ns\/)([a-z]\.[a-z0-9_]+)\>\t\<'
PATTERN_RETRIEVE_OBJECT_ID = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/)[a-z]\.[a-z0-9_]+'

PATTERN_ARTIST = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.artist\>|\<.*music\.artist.*\>\s+\<.*\>)'
PATTERN_ALBUM = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.album\>|\<.*music\.album.*\>\s+\<.*\>)'
PATTERN_RECORDING = r'\<.*\>\s+(\<.*(ns#type|type\.object\.type)\>\s+\<.*ns\/music\.recording\>|\<.*music\.recording.*\>\s+\<.*\>)'
PATTERN_GENRE = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.notable_for\.predicate\>\t+\"\/music\/(?P<type>artist|album)\/genre\"'

PATTERN_ALBUM_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.album\.artist\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_RECORDING_ARTIST = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/music\.recording\.artist\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_ARTIST_AWARDS_WON = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_winner\.awards_won\>\t+\<.*\/(?P<object_id>[gm].*)\>'

sys.path.append('.')

ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
GENRE = 'genre'
AWARD_HONOR = 'award_honor'

def getSubjectId(input):
    result = re.search(PATTERN_RETRIEVE_SUBJECT_ID, input)
    return None if result == None else result.group(1) 

def getObjectId(input):
    result = re.search(PATTERN_RETRIEVE_OBJECT_ID, input)
    return None if result == None else result.group(0) 

data = set()

last_award_honor = []

for line in sys.stdin:
    object_type = None
    
    if (re.match(PATTERN_ARTIST, line)):
        object_type = ARTIST
        if (len(last_award_honor) > 0 and last_award_honor[0] == getSubjectId(line)):
            data.add(last_award_honor[1])
            print(str(last_award_honor[1]) + "\t" + str(AWARD_HONOR))            
        else:
            last_award_honor = []
    elif (re.match(PATTERN_ARTIST_AWARDS_WON, line)):
        subject_id = getSubjectId(line)
        object_id = getObjectId(line)
        if subject_id in data and object_id not in data:
            data.add(object_id)
            print(str(object_id) + "\t" + str(AWARD_HONOR))
        else:
            last_award_honor = [getSubjectId(line), getObjectId(line)]
    elif (re.match(PATTERN_RECORDING, line)):
        object_type = TRACK
    elif (re.match(PATTERN_ALBUM, line)):
        object_type = ALBUM
    elif (re.match(PATTERN_GENRE, line)):
        object_type = GENRE

    if (object_type != None):    
        id = getSubjectId(line)
        if (id not in data):
            data.add(id)
            print(str(id) + "\t" + str(object_type))
