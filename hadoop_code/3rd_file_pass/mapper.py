#!/usr/bin/env python
"""mapper.py"""

import sys
import re
import jsonpickle
import os


# GENERAL
# Matching patterns
PATTERN_OBJECT_NAME = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.name\>\t+\"(?P<name>.*)\"@en'
PATTERN_OBJECT_DESCRIPTION = r'\<.*\>\t+\<http:\/\/rdf\.freebase\.com\/ns\/common\.topic\.description\>\t+\"(?P<description>.*)\"@en'

# Value retrieval patterns
PATTERN_RETRIEVE_SUBJECT_ID = r'(?<=\<http:\/\/rdf\.freebase\.com\/ns\/)([a-z]\.[a-z0-9_]+)\>\t\<'
PATTERN_RETRIEVE_OBJECT_ID = r'(?<!not )(?<=\t\<http:\/\/rdf\.freebase\.com\/ns\/)[a-z]\.[a-z0-9_]+'

PATTERN_AWARD_IDS = r'.*\"entity_type\": \"award_honor\"'

sys.path.append('.')

def getSubjectId(input):
    result = re.search(PATTERN_RETRIEVE_SUBJECT_ID, input)
    return None if result == None else result.group(1) 

def getObjectId(input):
    result = re.search(PATTERN_RETRIEVE_OBJECT_ID, input)
    return None if result == None else result.group(0) 

def handleCommon(data, line):
    if (re.match(PATTERN_OBJECT_NAME, line)):
        match = re.match(PATTERN_OBJECT_NAME, line)
        data['name'] = match.group('name')
    elif (re.match(PATTERN_OBJECT_DESCRIPTION, line)):
        match = re.match(PATTERN_OBJECT_DESCRIPTION, line)
        data['description'] = match.group('description')  
    return data

def handleAwardParsing(data, line, found_id):
    _data = data[found_id]
    _data = handleCommon(_data, line)
    return data

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
            entity_data = jsonpickle.decode(entity_data)
            data[entity_data['detail_reference']] = entity_data
        line = f.readline()
    f.close()
    return data

# fileName = './3rd_file_pass/input_100M'
fileName = 'input'
data = readIdsAndTypes(fileName)
previous_id = None
line_count = 0

for line in sys.stdin:
    found_id = getSubjectId(line)
    line_count+= 1
    if (found_id != None and found_id in data):
        data = handleAwardParsing(data, line, found_id)
        if (previous_id == None or (previous_id != None and previous_id != found_id)):
            if (previous_id != None):
                    printObject(data[previous_id]['id'], data[previous_id])
                    previous_id = None
            else:        
                previous_id = found_id
    if (line_count % 10000 == 0):
        print('')
if (previous_id != None):
    printObject(data[previous_id]['id'], data[previous_id])