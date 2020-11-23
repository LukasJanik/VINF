from elasticsearch import Elasticsearch, helpers

import json
import time
import os
import re

elastic = Elasticsearch(timeout=200)

index = -1

def loadFile(fileName):
    data = []
    with open(fileName) as file:
        line = file.readline()
        while line != '':
            data.append(line.strip())
            line = file.readline()
    return data

def bulk_json_data(fileName):
    data = loadFile(fileName)
    for artist in data:
        artist_id =  re.match(r'^\{\"id\": \"(?P<id>[a-zA-z.0-9_]*)\",', artist).group('id')
        yield {
            "_index": "music",
            "_id": artist_id,
            "_source": artist
        }

inputDataFolder = '../cluster_data_processing/final_output'
files = os.listdir(inputDataFolder)

for file in files:
    try:
        # make the bulk call, and get a response
        print(f"Processing file {file}")
        start_time = time.time()
        response = helpers.bulk(elastic, bulk_json_data(f"{inputDataFolder}/{file}"), chunk_size=1000)
        print ("\nbulk_json_data() RESPONSE:", response)
        print("--- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        print("\nERROR:", e)