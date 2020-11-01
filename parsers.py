from patterns import *
from models import Artist, Track, Album, TrackContribution, Award, Genre
from constants import ALBUM, ARTIST, AWARD, AWARD_INFO_TYPE_AWARD_WON, AWARD_INFO_TYPE_HONOR, TRACK, TRACK_CONTRIBUTION, GENRE, GENRE_MAPPER
import re

def getSubjectId(input: str):
    result = re.search(PATTERN_RETRIEVE_SUBJECT_ID, input)
    return None if result == None else result.group(1) 

def getObjectId(input: str):
    result = re.search(PATTERN_RETRIEVE_OBJECT_ID, input)
    return None if result == None else result.group(0) 

def getOrCreate(data: dict, entity: str, id: int):
    entity_instance = None
    if (id not in data[entity]):
        entity_instance = ENTITY_CREATION_BY_NAME[entity](id)
        data[entity][id] = entity_instance
    else:
        entity_instance = data[entity][id]
    return entity_instance, data

def handleArtistParsing(data, line: str, found_id: int):
    _data = data[ARTIST][found_id]
    if (match:=re.match(PATTERN_ARTIST_PEOPLE_PERSON_DATE_OF_BIRTH, line)):
        _data.date_of_birth = match.group('date')
    elif (match:=re.match(PATTERN_ARTIST_ACTIVE_START, line)):
        _data.active_start = match.group('date')
    elif (match:=re.match(PATTERN_ARTIST_ACTIVE_END, line)):
        _data.active_end = match.group('date')
    elif (match:=re.match(PATTERN_ARTIST_ORIGIN, line)):
        _data.origin = match.group('object_id')
    elif (match:=re.match(PATTERN_ARTIST_GENRE, line)):
        genre, data = getOrCreate(data, GENRE, match.group('object_id'))
        _data.genre = genre.id
    elif (match:=re.match(PATTERN_OBJECT_NAME, line)):
        _data.name = match.group('name')
    elif (match:=re.match(PATTERN_OBJECT_DESCRIPTION, line)):
        _data.description = match.group('description')        
    elif (match:=re.match(PATTERN_ARTIST_TRACK, line)):
        track, data = getOrCreate(data, TRACK, match.group('object_id'))
        _data.tracks.append(track.id)
    elif (match:=re.match(PATTERN_ARTIST_ALBUM, line)):
        album, data = getOrCreate(data, ALBUM, match.group('object_id'))
        _data.albums.append(album.id)
    # elif (re.match(PATTERN_ARTIST_TRACK_CONTRIBUTION, line)):
    #     track_contribution, data = getOrCreate(data, TRACK_CONTRIBUTION, getObjectId(line))
    #     _data.track_contributions.append(track_contribution)
    # elif (re.match(PATTERN_ARTIST_AWARD_NOMINATION, line)):
    #     award_nomination, data = getOrCreate(data, AWARD, getObjectId(line))
    #     award_nomination.noaward_honor = AWARD_INFO_TYPE_HONOR
    elif (match:=re.match(PATTERN_ARTIST_AWARDS_WON, line)):
        award_won, data = getOrCreate(data, AWARD, match.group('object_id'))
        award_won.object_type = AWARD_INFO_TYPE_AWARD_WON
        _data.awards_won.append(award_won.id)
    return data

def handleTrackParsing(data, line: str, found_id: int):
    _data = data[TRACK][found_id]
    if (match:=re.match(PATTERN_OBJECT_NAME, line)):
        _data.name = match.group('name')
    if (match:=re.match(PATTERN_OBJECT_DESCRIPTION, line)):
        _data.description = match.group('description')        
    elif (match:=re.match(PATTERN_RECORDING_ARTIST, line)):
        artist, data = getOrCreate(data, ARTIST, match.group('object_id'))
        # artist.tracks.append(_data)
        _data.artists.append(artist.id)
    elif (match:=re.match(PATTERN_RECORDING_LENGTH, line)):
        _data.length = match.group('length')
    # elif (re.match(PATTERN_AWARD_NOMINATED_WORK, line)):
    #     award_nominated_work, data = getOrCreate(data, AWARD, getObjectId(line))
    #     award_nominated_work.nomination_type = NOMINATION_TYPE_WORK
    #     _data.awards_nominated.append(award_nominated_work)
    return data

def handleAlbumParsing(data, line: str, found_id: int):
    _data = data[ALBUM][found_id]
    if (match:=re.match(PATTERN_OBJECT_NAME, line)):
        _data.name = match.group('name')
    elif (match:=re.match(PATTERN_OBJECT_DESCRIPTION, line)):
        _data.description = match.group('description')
    elif (match:=re.match(PATTERN_ALBUM_ARTIST, line)):
        artist, data = getOrCreate(data, ARTIST, match.group('object_id'))
        artist.albums.append(found_id)
        _data.artists.append(artist.id)
    elif (match:=re.match(PATTERN_ALBUM_RELEASE_DATE, line)):
        _data.release_date = match.group('date')
    # elif (re.match(PATTERN_AWARD_NOMINATED_WORK, line)):
    #     award_nominated_work, data = getOrCreate(data, AWARD, getObjectId(line))
    #     award_nominated_work.nomination_type = NOMINATION_TYPE_WORK
    #     _data.awards_nominated.append(award_nominated_work)        
    return data

def handleAwardParsing(data, line: str, found_id: int):
    _data = data[AWARD][found_id]
    if(match:=re.match(PATTERN_AWARD_HONOR_AWARD, line)):
        award_honor_award, data = getOrCreate(data, AWARD, match.group('object_id'))
        award_honor_award.object_type = AWARD_INFO_TYPE_HONOR
        _data.detail_object = award_honor_award
    elif(match:=re.match(PATTERN_OBJECT_NAME, line)):
        _data.name = match.group('name')
    elif(match:=re.match(PATTERN_OBJECT_DESCRIPTION, line)):
        _data.description = match.group('description')
    return data

def handleGenreParsing(data, line:str, found_id: int):
    _data = data[GENRE][found_id]
    if (match := re.match(PATTERN_GENRE_NAME, line)):
        _data.name = match.group('name')
    return data

def handleInitialParsing(data, line):
    object_type = None

    if (re.match(PATTERN_ARTIST, line)):
        object_type = ARTIST
    elif (re.match(PATTERN_RECORDING, line)):
        object_type = TRACK
    elif (re.match(PATTERN_ALBUM, line)):
        object_type = ALBUM
    elif (re.match(PATTERN_GENRE, line)):
        object_type = GENRE

    if (object_type != None):    
        result, data = getOrCreate(data, object_type, getSubjectId(line))
        if (object_type == GENRE):
            result.genre_type = re.match(PATTERN_GENRE, line).group('type')

    return data

def handleSecondaryParsing(data, line):
    found_id = getSubjectId(line)
    if (found_id != None):
        if (found_id in data[ARTIST]):
            data = handleArtistParsing(data, line, found_id)
        elif (found_id in data[ALBUM]):
            data = handleAlbumParsing(data, line, found_id)
        elif (found_id in data[TRACK]):
            data = handleTrackParsing(data, line, found_id)
        elif (re.match(PATTERN_AWARD_HONOR_AWARD_WINNER, line)):
            object_id = getObjectId(line)
            if (object_id in data[ARTIST]):
                award, data = getOrCreate(data, AWARD, found_id)
                data[ARTIST][object_id].awards_won.append(award)
    return data

def handleTertiaryParsing(data, line):
    found_id = getSubjectId(line)
    if (found_id != None): 
        if (found_id in data[AWARD]):
            data = handleAwardParsing(data, line, found_id)
        elif (found_id in data[GENRE]):
            data = handleGenreParsing(data, line, found_id)
    return data

ENTITY_PARSING_BY_NAME = {
    'artist': handleArtistParsing,
    'track': handleTrackParsing,
    'album': handleAlbumParsing
}

ENTITY_CREATION_BY_NAME = {
    'artist': Artist,
    'track': Track,
    'album': Album,
    'track_contribution': TrackContribution,
    'award': Award,
    'genre': Genre
}