import jsonpickle
import json
import sys
import numpy as np
from models import *

ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
GENRE = 'genre'
AWARD = 'award_honor'

def max_statistics(statistics, length, name, id):
    statistics['max_value'] = length
    statistics['artists'].append({
        'id': id,
        'name': name,
        'value': length
        })
    statistics['artists'] = statistics['artists'][-5:]
    return statistics

def getStatistics(data):
    return {
        'with_0': len(data) - np.count_nonzero(data),
        'max:': max(data),
        'mean': np.mean(data),
        'min': min(data),
        'med': np.median(data)
    }


def loadArtists():
    with open(f"./filtered_output/artist/artist_0.json", "r") as file:
        return json.load(file)

def loadGenres():
    with open(f"./filtered_output/genre/genre_0.json", "r") as file:
        return json.load(file)

def loadAlbums():
    dict_1 = None
    dict_2 = None
    with open(f"./filtered_output/album/album_0.json", "r") as file:
        dict_1 = json.load(file)
    with open(f"./filtered_output/album/album_0.json", "r") as file:
        dict_2 = json.load(file)
    return dict(dict_1, **dict_2)

def loadAwards():
    with open(f"./filtered_output/award_honor/award_honor_0.json", "r") as file:
        return json.load(file)

def loadTracks(id:int):
    with open(f"./filtered_output/track/track_{id}.json", "r") as file:
        return json.load(file)

def createFinalArtists(artists_tmp):

    statistics['artists']['total'] = len(artists_tmp)

    artists_final = dict()

    album_to_artist = dict()
    track_to_artist = dict()
    award_to_artist = dict()
    genre_to_artist = dict()

    for artist in artists_tmp:
        tmp_artist = artists_tmp[artist]

        artist_to_albums = tmp_artist["albums"]
        artist_to_tracks = tmp_artist["tracks"]
        artist_to_awards = tmp_artist["awards_won"]
        # artist_genre = tmp_artist["genre"]
        
        artist_id = tmp_artist["id"]

        artists_final[artist_id] = Artist(
            artist_id,
            tmp_artist['name'],
            tmp_artist['description'],
            tmp_artist['active_start'],
            tmp_artist['active_end'],
            tmp_artist['date_of_birth']
        )

        for album in artist_to_albums:
            if (album not in album_to_artist):
                album_to_artist[album] = [artist_id]
            else:
                album_to_artist[album].append(artist_id)

        for track in artist_to_tracks:
            if (track not in track_to_artist):
                track_to_artist[track] = [artist_id]
            else:
                track_to_artist[track].append(artist_id)
        
        for award in artist_to_awards:
            if (award not in award_to_artist):
                award_to_artist[award] = [artist_id]
            else:
                award_to_artist[award].append(artist_id)

    return artists_final, album_to_artist, track_to_artist, award_to_artist, genre_to_artist

def fillAlbums(artists_final, album_to_artist):
    print('Loading Albums')
    albums = loadAlbums()
    statistics['albums']['total'] = len(albums)
    print('Filling albums')
    for album in albums:
        album_tmp = albums[album]
        album_final = Album(
            album_tmp['id'],
            album_tmp['name'],
            album_tmp['description'],
            album_tmp['release_date']
        )
        
        artist_list = album_tmp['artists']
        if (album_tmp['id'] in album_to_artist):
            artist_list = set(artist_list + album_to_artist[album_tmp['id']])
            
        for artist in artist_list:
            if (artist in artists_final):
                artists_final[artist].albums.append(album_final)

                statistics['albums']['name'].append(0 if album_final.name == None else len(album_final.name))
                statistics['albums']['description'].append(0 if album_final.description == None else len(album_final.description))

                if (album_final.release_date == None):
                    statistics['albums']['without_release_date'] += 1

            else:
                statistics['albums']['without_artist'] += 1

def fillAwards(artists_final, award_to_artist):
    print('Loading Awards')
    awards = loadAwards()
    statistics['awards']['total'] = len(awards)
    print('Filling Awards')
    for award in awards:
        award_tmp = awards[award]
        award_final = Award(
            award_tmp['id'],
            award_tmp['name'],
            award_tmp['description'],
        )
        
        if (award_tmp['id'] in award_to_artist):
            artist_list = award_to_artist[award_tmp['id']]
            for artist in artist_list:
                if(artist in artists_final):
                    artists_final[artist].awards_won.append(award_final)

                    statistics['awards']['name'].append(0 if award_final.name == None else len(award_final.name))
                    statistics['awards']['description'].append(0 if award_final.description == None else len(award_final.description))

                else:
                    statistics['awards']['without_artist'] += 1

def fillTracks(artists_final, track_to_artist, number_of_track_bulks):
    for track_bulk in range(number_of_track_bulks):
        print(f"Loading Tracks {track_bulk}")
        tracks = loadTracks(track_bulk)
        statistics['tracks']['total'] += len(tracks)
        print(f"Filling Tracks {track_bulk}")
        for track in tracks:
            track_tmp = tracks[track]
            track_final = Track(
                track_tmp['id'],
                track_tmp['name'],
                track_tmp['description']
            )
            
            artist_list = track_tmp['artists']
            if (track_tmp['id'] in track_to_artist):
                artist_list = set(artist_list + track_to_artist[track_tmp['id']])
                
            for artist in artist_list:
                if (artist in artists_final):
                    artists_final[artist].tracks.append(track_final)

                    statistics['tracks']['name'].append(0 if track_final.name == None else len(track_final.name))
                    statistics['tracks']['description'].append(0 if track_final.description == None else len(track_final.description))

                else:
                    statistics['tracks']['without_artist'] += 1

def writeFinalArtists(artists_final):
    count = 0
    file = None
    file_index = 0
    
    print('Saving artists')
    for artist in artists_final:
        if (count == 0 or count % 50000 == 0):
            if (file != None):
                file.close()
            file = open(f"./final_output/artist_{file_index}.json", "w")
            file_index += 1
        
        tracks_length = len(artists_final[artist].tracks)
        albums_length = len(artists_final[artist].albums)
        awards_won_length = len(artists_final[artist].awards_won)

        # Statistics

        artists_final[artist].no_of_tracks = tracks_length 
        statistics['artists']['tracks'].append(tracks_length)

        if (tracks_length >= statistics['artists']['max_tracks']['max_value']):
            statistics['artists']['max_tracks'] = max_statistics(
                statistics['artists']['max_tracks'],
                tracks_length,
                artists_final[artist].name,
                artists_final[artist].id
            )

        artists_final[artist].no_of_albums = albums_length
        statistics['artists']['albums'].append(albums_length)

        if (albums_length >= statistics['artists']['max_albums']['max_value']):
            statistics['artists']['max_albums'] = max_statistics(
                statistics['artists']['max_albums'],
                tracks_length,
                artists_final[artist].name,
                artists_final[artist].id
            )

        artists_final[artist].no_of_awards_won = awards_won_length
        statistics['artists']['awards'].append(awards_won_length)

        if (awards_won_length >= statistics['artists']['max_awards']['max_value']):
            statistics['artists']['max_awards'] = max_statistics(
                statistics['artists']['max_awards'],
                tracks_length,
                artists_final[artist].name,
                artists_final[artist].id
            )
        
        statistics['artists']['name'].append(0 if artists_final[artist].name == None else len(artists_final[artist].name))
        
        statistics['artists']['description'].append(0 if artists_final[artist].description == None else len(artists_final[artist].description))

        if (artists_final[artist].active_start == None):
            statistics['artists']['without_active_start'] += 1
        
        if (artists_final[artist].active_end == None):
            statistics['artists']['without_active_end'] += 1

        if (artists_final[artist].date_of_birth == None):
            statistics['artists']['without_date_of_birth'] += 1

        file.write(f"{jsonpickle.encode(artists_final[artist], unpicklable=False)}\n")
        count += 1
    if (file != None and not file.closed):
        file.close()

statistics = {
    'artists': {
        'name': [], #
        'description': [], #
        'without_active_start': 0, #
        'without_active_end': 0, #
        'without_date_of_birth': 0, #
        'tracks': [], 
        'awards': [], 
        'albums': [], 
        'max_tracks': {  #
            'max_value': 0,
            'artists': []
        },
        'max_albums': { #
            'max_value': 0,
            'artists': []
        },
        'max_awards': { #
            'max_value': 0,
            'artists': []
        },
        'total': 0
    },
    'tracks': {
        'without_artist': 0, 
        'name': [], #
        'description': [], #
        'total': 0
    },
    'albums': {
        'name': [], #
        'description': [], #
        'without_artist': 0, # 
        'without_release_date': 0,
        'total': 0
    },    
    'awards': {
        'name': [], #
        'description': [], #
        'without_artist': 0, # 
        'total': 0
    }
}

artists_tmp = loadArtists()
artists_final, album_to_artist, track_to_artist, award_to_artist, genre_to_artist = createFinalArtists(artists_tmp)

# fillGenre(artists_final, genre_to_artist)
fillAlbums(artists_final, album_to_artist)
fillAwards(artists_final, award_to_artist)
fillTracks(artists_final, track_to_artist, 11)

writeFinalArtists(artists_final)

statistics['artists']['tracks'] = getStatistics(statistics['artists']['tracks'])
statistics['artists']['awards'] = getStatistics(statistics['artists']['awards'])
statistics['artists']['albums'] = getStatistics(statistics['artists']['albums'])

statistics['artists']['name'] = getStatistics(statistics['artists']['name'])
statistics['artists']['description'] = getStatistics(statistics['artists']['description'])

statistics['tracks']['name'] = getStatistics(statistics['tracks']['name'])
statistics['tracks']['description'] = getStatistics(statistics['tracks']['description'])

statistics['albums']['name'] = getStatistics(statistics['albums']['name'])
statistics['albums']['description'] = getStatistics(statistics['albums']['description'])

statistics['awards']['name'] = getStatistics(statistics['awards']['name'])
statistics['awards']['description'] = getStatistics(statistics['awards']['description'])


file = open('statistics.json', 'w')
file.write(jsonpickle.encode(statistics, unpicklable=False))
file.close()