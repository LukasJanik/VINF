from elasticsearch import Elasticsearch, helpers
from functools import partial
import re, json, textwrap

elastic = Elasticsearch()

initial_string = """
Freebase Artists & Awards & Tracks Index search:
==============================================================================================================================================================
Form:
-switch "property = value", for list of properties: "property1 = value; property2 = value"
Options:
-a for match (AND)
-o for match (OR)
-r for <greater than or equal to, less than or equal to> (special cases - date: YYYY-MM-DD, undefined value: NONE)
-t for textsearch (fulltext)
-s for scoring: no_of_albums | no_of_awards_won | no_of_tracks (default)

-p for list of properties to retrieve
-l for limiting number of results 

-f for reading elasticsearch valid query from file
-i for displaying statistical info
-q for quiting
==============================================================================================================================================================

Input:
"""
def getBasicQueryBody(limit: int) -> dict:
    return {
        "size": limit,
        "query": {
            "bool": {}
        }
    }

def getInputs(_input: str, key: str, ignore_empty=False) -> []:
    if key in _input or ignore_empty:
        results = list(filter(None, _input.split(key)))
        return list(map(lambda result: result.strip(), results))
    return None

def getValues(_input: str, _type: str, custom_regex=None) -> str:
    match = re.match(rf".*-{_type} (?P<match>[^\?]*)\?" if custom_regex == None else custom_regex, _input)
    return match.group('match') if match != None else None
    
def buildParams(_input: str, _range=False) -> []:
    final_params = []

    params = getInputs(_input, ';', True)

    for param in params:
        key, value = getInputs(param, '=')
        
        key = key.replace('artist.', '') if 'artist' in key else key    

        if (not _range):
            match = {'match': {}}
            match['match'][key] = value
            final_params.append(match)
        else:
            date = key in ['active_end', 'active_start', 'date_of_birth', 'release_date']
            __range = getRange(key, value, date)
            if (__range != None):
                final_params.append(__range)
    return final_params

def getRange(_key: str, _range: str, date = False) -> dict:
    __range = {'range': {}}
    regex = None 
    value1 = None
    value2 = None

    if (date):
        regex = r'<(?P<value1>[0-9]{4}[-]{0,1}[0-9]{0,2}[-]{0,1}[0-9]{0,2}|NONE), (?P<value2>[0-9]{4}[-]{0,1}[0-9]{0,2}[-]{0,1}[0-9]{0,2}|NONE)>'
    else:
        regex = r'<(?P<value1>[0-9]*|NONE), (?P<value2>[0-9]*|NONE)>' 
    match = re.match(
            regex, 
            _range,
            re.IGNORECASE
        )
    if (match == None):
        return None

    if (match.group('value1') != None and  match.group('value1') != 'NONE'):
        value1 = processDate(match.group('value1')) if date else match.group('value1')
    if (match.group('value2') != None and  match.group('value2') != 'NONE'):        
        value2 = processDate(match.group('value2')) if date else match.group('value2')

    if (value1 == None and value2 == None):
        return None
    else:
        __range['range'][_key] = {}
        if (value1 != None):
            __range['range'][_key]['gte'] = value1
        if (value2 != None):
            __range['range'][_key]['lte'] = value2

    return __range 

def processDate(_date: str) -> str:
    if _date == 'NONE':
        return None
    else:
        date = _date.split('-')
        if (len(date) == 1):
            return f"{date[0]}-01-01"
        else:
            return f"{date[0]}-01"

def buildQuery(_input:str, limit = 10) -> dict:
    basic_query = getBasicQueryBody(limit)
    
    _getValues = partial(getValues, _input)

    ands = _getValues('a')
    ors = _getValues('o')
    _range = _getValues('r')
    props = _getValues('p')

    if (ands != None or ors != None or _range != None or props != None):
        if (ands != None):
            basic_query['query']['bool']['must'] = buildParams(ands)
        if (ors != None):
            basic_query['query']['bool']['should'] = buildParams(ors)
        if (_range):
            if ('must' not in basic_query['query']['bool']):
                basic_query['query']['bool']['must'] = []
            __range = buildParams(_range, True)
            if (__range != None):
                for ___range in __range:
                    basic_query['query']['bool']['must'].append(___range)
        if (props != None):
            basic_query['fields'] = [prop if 'artist' not in prop else prop.replace('artist.', '') for prop in getInputs(props, ',', True)]
        return basic_query
    return None

def fulltextQuery(_input: str, limit: int) -> dict:
    values = getValues(_input, 't')
    props = getValues(_input, 'p')
    
    query = {
        "size": limit,
        "query": {
            "query_string": {
                "query": values
            }
        }
    }

    if (props != None):
        query['fields'] = [prop if 'artist' not in prop else prop.replace('artist.', '') for prop in getInputs(props, ',', True)]

    return query

def handleScoring(_input: str, query: dict) -> dict:
    regex = r'.*-s (?P<match>no_of_albums|no_of_awards_won|no_of_tracks[^\?]*)\?'
    scoring_attribute = getValues(_input, '', regex)

    finalQuery = {
        "size": query['size'],
        "query": {
            "function_score": {
                "query": {i:query['query'][i] for i in query['query'] if i!='fields'},
                "script_score": {
                    "script": {
                        "source": f"doc['{scoring_attribute if scoring_attribute != None else 'no_of_tracks'}'].value"
                    }
                }
            }
        }
    }

    if 'fields' in query:
        finalQuery['fields'] = query['fields']
    
    return finalQuery

def printNestedStatistics(key1: str, key2: str, statistics: dict, label = None) -> None:
    print(f"\n{key1}:")
    print(f"\tNot filled: {statistics[key1]['with_0']}")
    print(f"\tMax {'number of characters' if label == None else label}: {statistics[key1][key2]['max']}")
    print(f"\tMin {'number of characters' if label == None else label}: {statistics[key1][key2]['min']}")
    print(f"\tMean {'number of characters' if label == None else label}: {statistics[key1][key2]['mean']}")
    print(f"\tMedian {'number of characters' if label == None else label}: {statistics[key1][key2]['med']}")

def printMax(key: str, statistics: dict) -> None:
    print(f"\n{key}:")
    print(f"\t{key} per artist: {statistics[key]['max_value']}")
    array_size = len(statistics[key]['artists'])
    for artist, index in zip(reversed(statistics[key]['artists']), range(array_size)):
        print(f"\t{index+1}. id: {artist['id']}, name: {artist['name']}, value: {artist['value']}")
    
def printStatistics(statistics: dict) -> None:
    for key in statistics:
        print('\n===============================================================================')
        print (f"                                   {key}:")
        print("===============================================================================")
        print (f"Total number of records: {statistics[key]['total']}")
        printNestedStatistics("name", "length", statistics[key])
        printNestedStatistics("description", "length", statistics[key])

        if (key == "ARTISTS"):
            printNestedStatistics('albums', "albums_per_artist", statistics[key], "albums_per_artist")
            printNestedStatistics('awards', "awards_per_artist", statistics[key], "awards_per_artist")
            printNestedStatistics('tracks', "tracks_per_artist", statistics[key], "tracks_per_artist")
            
            printMax('max_albums', statistics[key])
            printMax('max_awards', statistics[key])
            printMax('max_tracks', statistics[key])

            print(f"\nNot filled:")
            for not_filled in statistics[key]['not_filled']:
                print(f"\t{not_filled}: {statistics[key]['not_filled'][not_filled]}")
        
        if (key == "ALBUMS"):
            print(f"No release_date: {statistics[key]['without_release_date']}")

        if (key in ["TRACKS", "ALBUMS", "AWARDS"]):
            print (f"\nNo artists found: {statistics[key]['without_artist']}")
            
def handleQueryFile(_input:str) -> dict:
    fileName = re.match(r'-f (?P<fileName>.*)\.json', _input)
    fileName = fileName.group('fileName') if fileName != None else None
    if (fileName != None):
        with open(f"./queries/{fileName}.json", 'r') as queryFile:
            return json.load(queryFile)
    return None

def printResult(index: int, result: dict, limit: int):
    print(f"\n{index + 1}. ARTIST:")

    for key in result:
        if (key not in ['albums', 'awards_won', 'tracks']):
            if (key == 'description' and result[key] != None):
                print(f"\t{key}:")
                print(wrapper1.fill(result[key]))
            else:
                left = f"{key}:".ljust(20)
                print(f"\t{left}{result[key]}")
        else:
            print(f"\t{key}:")
            limited = result[key][:limit]
            for entity, index in zip(limited, range(limit)):
                if (len(limited) > 1):
                    print(f"\t\t{index + 1}.")
                for key2 in entity:
                    left = f"{key2}:".ljust(20)
                    if (key2 == 'description' and entity[key2] != None):
                        print(f"\t\t{key2.format(width=20)}:")
                        print(wrapper2.fill(entity[key2]))
                    else:
                        print(f"\t\t{left}{entity[key2]}")

statistics = None
indent_1 = '\t' + ' ' * 20
indent_2 = '\t' + indent_1
wrapper1 = textwrap.TextWrapper(initial_indent=indent_1, subsequent_indent=indent_1, width=80)
wrapper2 = textwrap.TextWrapper(initial_indent=indent_2, subsequent_indent=indent_2, width=80)
separator = "=============================================================================================================================================================="

with open('statistics_formatted.json', 'r') as file:
    statistics = json.load(file)

while True:
    limit = 10
    _input = input(initial_string)
    if '-q' in _input:
        print('bye')
        break
    elif '-i' in _input:
        printStatistics(statistics)
    else:
        query = None
        if '-l' in _input:
            limit = re.match(r'.*-l (?P<limit>[0-9]*)', _input)
            limit = limit.group('limit')
            limit = int(limit) if limit != None else 10

        if '-f' in _input:
            query = handleQueryFile(_input)
        elif '-t' in _input:
            query = fulltextQuery(_input, limit)
        else:   
            query = buildQuery(_input, limit)
        
        if '-s' in _input: 
            query = handleScoring(_input, query)

        if (query != None):
            value = elastic.search(index="music", body=query)
            print(f"\n{separator}")
            print("                                                                     Results")
            print(separator)
            if (value != None):
                source = value['hits']['hits'] if limit == None else value['hits']['hits'][:limit]
                for hit, index in zip(source, range(len(source))):
                    if ('fields' in query and 'fields' in hit) or ('fields' not in query):
                        if (index != 0):
                            print(separator)                        
                        if 'fields' in query and 'fields' in hit:
                            printResult(index, hit['fields'], limit)    
                        elif 'fields' not in query:
                            printResult(index, hit['_source'], limit)
