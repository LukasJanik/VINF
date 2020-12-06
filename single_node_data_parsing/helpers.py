
from constants import ALBUM, ARTIST, AWARD, TRACK, GENRE, OUTPUT_DIR
from parsers import handleArtistParsing, handleAlbumParsing, handleTrackParsing
import re
import json
from json import JSONEncoder
import jsonpickle
import os

def initializeDict():
    data = dict()
    data[ARTIST] = dict()
    data[TRACK] = dict()
    data[ALBUM] = dict()
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
