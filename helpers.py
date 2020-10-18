
from constants import ALBUM, ARTIST, AWARD, RECORDING, TRACK, TRACK_CONTRIBUTION, GENRE, OUTPUT_FILE
from parsers import handleArtistParsing, handleAlbumParsing, handleRecordingParsing
import re
import json

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
        json.dump(data[key], output_file) 
        output_file.write("\n")
    print ('Data saved')
