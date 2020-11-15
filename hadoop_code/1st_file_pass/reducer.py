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
entity_type = None
curr_id = None
line_count = 0
# input comes from STDIN
for line in sys.stdin:
    line = line.strip()

    if (id == None):
        id, entity_type = line.split('\t', 1)

    curr_id, curr_entity_type = line.split('\t', 1)

    if curr_id != id:
        print(str(id) + "\t" + str(entity_type))
        id = curr_id
        entity_type = curr_entity_type
    
if curr_id == id:
    print(str(id) + "\t" + str(entity_type))
