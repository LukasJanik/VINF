
from constants import ALBUM, ARTIST, AWARD, RECORDING, TRACK, TRACK_CONTRIBUTION, GENRE, OUTPUT_FILE
from parsers import handleArtistParsing, handleAlbumParsing, handleRecordingParsing
import re
import json
from json import JSONEncoder
import jsonpickle

def ComplexHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))

def initializeDict():
    data = dict()
    data[ARTIST] = dict()
    data[TRACK] = dict()
    data[ALBUM] = dict()
    data[TRACK_CONTRIBUTION] = dict()
    data[RECORDING] = dict()
    data[AWARD] = dict()
    data[GENRE] = dict()
    return data

def saveData(data):
    output_file = open(OUTPUT_FILE, 'w', encoding='utf-8')
    for key in data:
        jsonData = jsonpickle.encode(data[key], unpicklable=False)
        output_file.write(f"{key}:{jsonData}\n")
    print ('Data saved')
