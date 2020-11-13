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
AWARD_INFO_TYPE_HONOR = 'award_honor'

# AWARD
PATTERN_AWARD_HONOR_AWARD = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_honor\.award\>\t+\<.*\/(?P<object_id>[gm].*)\>'
PATTERN_AWARD_HONOR_AWARD_WINNER = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/award\.award_honor\.award_winner\>\t+\<.*\/(?P<object_id>[gm].*)\>'

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

PATTERN_AWARD_IDS = r'.*\"entity_type\": \"award\"'




sys.path.append('.')

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
        print('here\t' + match.group('name'))
        data.name = match.group('name')
    elif (re.match(PATTERN_OBJECT_DESCRIPTION, line)):
        match = re.match(PATTERN_OBJECT_DESCRIPTION, line)
        print('here\t' + match.group('description'))
        data.description = match.group('description')  
    return data

def handleAwardParsing(data, line, found_id, additional_award_entities):
    _data = data[found_id]
    _data = handleCommon(_data, line)
    if(re.match(PATTERN_AWARD_HONOR_AWARD, line)):
        match = re.match(PATTERN_AWARD_HONOR_AWARD, line)
        award_honor_award, data = getOrCreate(data, AWARD, match.group('object_id'))
        award_honor_award.object_type = AWARD_INFO_TYPE_HONOR
        _data['detail_object'] = award_honor_award
        data[match.group('object_id')] = award_honor_award
        additional_award_entities[match.group('object_id')] = found_id
    return data, additional_award_entities

ENTITY_CREATION_BY_NAME = {
    'award': Award
}

def printObject(id, _object):
    jsonData = jsonpickle.encode(_object, unpicklable=False)
    print(str(id) + '\t' + str(jsonData))

def readIdsAndTypes(fileName):
    data = dict()
    f = open(fileName, "r")
    line = f.readline()
    while line != '':
        if (re.match(PATTERN_AWARD_IDS, line)):
            curr_id, entity_data = line.rstrip().split('\t', 1)
            data[curr_id] = jsonpickle.decode(entity_data)
        line = f.readline()
    f.close()
    return data

# fileName = './3rd_file_pass/input_100M'
fileName = 'input_100M'
data = readIdsAndTypes(fileName)
previous_id = None


freebase = '../freebase-head-100000000'

additional_award_entities = dict()

# with open(freebase, "r", encoding="utf8") as file:
#     line = file.readline()
#     while line != '':
#         found_id = getSubjectId(line)
#         if (found_id != None and (found_id in data or found_id in additional_award_entities)):
#             data, additional_award_entities = handleAwardParsing(data, line, found_id, additional_award_entities)
#             if (previous_id == None or (previous_id != None and previous_id != found_id)):
#                 if (previous_id != None):
#                     if (previous_id in additional_award_entities):
#                         printObject(additional_award_entities[previous_id], data[additional_award_entities[previous_id]])        
#                     else:
#                         printObject(previous_id, data[previous_id])
#         line = file.readline()

for line in sys.stdin:
    found_id = getSubjectId(line)
    if (found_id != None and (found_id in data or found_id in additional_award_entities)):
        data, additional_award_entities = handleAwardParsing(data, line, found_id, additional_award_entities)
        if (previous_id == None or (previous_id != None and previous_id != found_id)):
            if (previous_id != None):
                if (previous_id in additional_award_entities):
                    printObject(additional_award_entities[previous_id], data[additional_award_entities[previous_id]])        
                else:
                    printObject(previous_id, data[previous_id])
            previous_id = found_id