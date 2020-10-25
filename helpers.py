
from constants import ALBUM, ARTIST, AWARD, TRACK, TRACK_CONTRIBUTION, GENRE, OUTPUT_DIR
from parsers import handleArtistParsing, handleAlbumParsing, handleTrackParsing
import re
import json
from json import JSONEncoder
import jsonpickle
import os

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
    # data[TRACK_CONTRIBUTION] = dict()
    data[AWARD] = dict()
    data[GENRE] = dict()
    return data

def saveData(data):
    try:
        print('Creating output folder')
        os.mkdir(OUTPUT_DIR)
    except:
        print('Folder already exists')
    for key in data:
        with open(f"./{OUTPUT_DIR}/{key}", 'w') as output_file:
            for item in data[key]:
                jsonData = jsonpickle.encode(data[key][item], unpicklable=False)
                output_file.write(f"{jsonData}\n")
    print ('Data saved')
