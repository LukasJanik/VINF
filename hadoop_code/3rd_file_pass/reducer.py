#!/usr/bin/env python
"""reducer.py"""

from operator import itemgetter
import jsonpickle
import sys
sys.path.append('.')

current_word = None
current_count = 0
word = None

id = None
data = None

curr_id = None
curr_data = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    if (id == None):
        id, data = line.split('\t', 1)
        data = jsonpickle.decode(data)

    curr_id, curr_data = line.split('\t', 1)
    curr_data = jsonpickle.decode(curr_data)

    if curr_id == id:
        for (key, value) in curr_data.items():
            data[key] = curr_data[key] if curr_data[key] != None else data[key]
    else:
        print(str(id) + "\t" + str(jsonpickle.encode(data, unpicklable=False)))
        id = curr_id
        data = curr_data
    
if curr_id == id:
    print(str(id) + "\t" + str(jsonpickle.encode(data, unpicklable=False)))
    