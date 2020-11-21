import jsonpickle
import sys

ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
GENRE = 'genre'
AWARD = 'award_honor'

def initializeDictAndCounters():
    data = dict()
    counters = dict()

    data[ARTIST] = dict()
    data[TRACK] = dict()
    data[ALBUM] = dict()
    data[GENRE] = dict()

    counters[ARTIST] = 0
    counters[TRACK] = 0
    counters[ALBUM] = 0
    counters[GENRE] = 0

    return data, counters

def writeToFile(fileName, data, counter):
    with open(f"./filtered_output/{fileName}/{fileName}_{counter}.json", "w") as file:
        file.write(jsonpickle.encode(data))

def createDictionairesByTypes(data, counters, all=False):
    for key in data:
        if len(data[key]) == 1000000 or all:
            writeToFile(key, data[key], counters[key])
            counters[key] += 1
            data[key] = dict()
    return data, counters


def handle_awards():
    data = dict()
    with open("filtered_awards", "r") as f:
        line = f.readline()
        while line != '':
            id, entity_data = line.rstrip().split('\t', 1)
            entity_data = jsonpickle.decode(entity_data)
            data[id] = entity_data
            line = f.readline()
    writeToFile('award_honor', data, 0)

def handle_rest():
    data, counters = initializeDictAndCounters()
    count = 0
    with open("filtered_all_data", "r", encoding="utf-8") as f:
        line = f.readline()
        while line != '':
            count += 1
            id, entity_data = line.rstrip().split('\t', 1)
            entity_data = jsonpickle.decode(entity_data)
            data[entity_data['entity_type']][id] = entity_data
            data, counters = createDictionairesByTypes(data, counters)
            if (count % 100000 == 0):
                print(count)
            line = f.readline()
    createDictionairesByTypes(data, counters, True)

# handle_rest()
handle_awards()