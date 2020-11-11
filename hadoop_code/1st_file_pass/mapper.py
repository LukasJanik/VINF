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


sys.path.append('.')

ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
GENRE = 'genre'

def getSubjectId(input):
    result = re.search(PATTERN_RETRIEVE_SUBJECT_ID, input)
    return None if result == None else result.group(1) 

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
        id = getSubjectId(line)
        if (id not in data):
            data.add(id)
            # TODO toto treba doriesit
            # if (object_type == GENRE):
                # entity_instance.genre_type = re.match(PATTERN_GENRE, line).group('type')
            print(str(id) + "\t" + str(object_type))
