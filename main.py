from os import listdir
import gzip
import json
import re

from parsers import handleAlbumParsing, handleArtistParsing, handleAwardParsing, handleInitialParsing, handleRecordingParsing, handleSecondaryParsing, handleTertiaryParsing
from constants import STATE, INITIAL_PARSING, SECONDARY_PARSING
from helpers import initializeDict, saveData

file = 'freebase-head-1000000'
# file = 'freebase-head-100000000'

f = open(file, "r", encoding="utf8")
line = f.readline()

line_counter: int = 0

data = initializeDict()

for i in range(3):
    f = open(file, "r", encoding="utf8")
    line = f.readline()
    line_counter = 0
    while (line != ''):
        if (STATE[i] == INITIAL_PARSING):
            data = handleInitialParsing(data, line)
        elif (STATE[i] == SECONDARY_PARSING):
            data = handleSecondaryParsing(data, line)
        else:
            data = handleTertiaryParsing(data, line)
        line_counter += 1
        if (line_counter % 100000 == 0):
            print(line_counter)
        line = f.readline()
print('the end of parsing')
saveData(data)