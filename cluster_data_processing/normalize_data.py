import jsonpickle
import json
import sys
from models import *

ARTIST = 'artist'
TRACK = 'track'
ALBUM = 'album'
GENRE = 'genre'
AWARD = 'award_honor'

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
        # if (artist_genre != None):    
        #     if (artist_genre not in genre_to_artist):
        #         genre_to_artist[artist_genre] = [artist_id]
        #     else:
        #         genre_to_artist[artist_genre].append(artist_id)

    return artists_final, album_to_artist, track_to_artist, award_to_artist, genre_to_artist

# def fillGenre(artists_final: dict, genre_to_artist: dict):
#     genres = loadGenres()
    
#     for genre in genres:
#         genre_id = genres[genre]['id']
#         if (genre_id in genre_to_artist):
#             for artist in genre_to_artist[genre_id]:
#                 artists_final[artist].genre = genres[genre]['name']

def fillAlbums(artists_final, album_to_artist):
    albums = loadAlbums()

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
            artists_final[artist].albums.append(album_final)

def fillAwards(artists_final, award_to_artist):
    awards = loadAwards()

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
                artists_final[artist].awards_won.append(award_final)

def fillTracks(artists_final, track_to_artist, number_of_track_bulks):
    count = 0
    for track_bulk in range(number_of_track_bulks):
        tracks = loadTracks(track_bulk)

        for track in tracks:
            track_tmp = tracks[track]
            track_final = Track(
                track_tmp['id'],
                track_tmp['name'],
                track_tmp['description'],
                track_tmp['length'],
            )
            
            artist_list = track_tmp['artists']
            if (track_tmp['id'] in track_to_artist):
                artist_list = set(artist_list + track_to_artist[track_tmp['id']])
                
            for artist in artist_list:
                if (artist in artists_final):
                    artists_final[artist].tracks.append(track_final)
                else:
                    count += 1
    print(f"Tracks without artists: {count}")

def writeFinalArtists(artists_final):
    count = 0
    file = None
    file_index = 0
    
    # length = len(artists_final)
    # number_of_files = length / 50000 if length % 50000 == 0 else (length / 50000) + 1
    
    # for file_index in range(number_of_files):
    #     with open(f"./final_output/artist_{file_index}.json", "w") as file:
    #         return json.load(file)
    
    for artist in artists_final:
        if (count == 0 or count % 50000 == 0):
            if (file != None):
                file.close()
            file = open(f"./final_output/artist_{file_index}.json", "w")
            file_index += 1
        file.write(f"{jsonpickle.encode(artists_final[artist])}\n", unpicklable=False)
        count += 1
    if (file != None and not file.closed):
        file.close()

artists_tmp = loadArtists()
artists_final, album_to_artist, track_to_artist, award_to_artist, genre_to_artist = createFinalArtists(artists_tmp)

fillGenre(artists_final, genre_to_artist)
# fillAlbums(artists_final, album_to_artist)
# fillAwards(artists_final, award_to_artist)
# fillTracks(artists_final, track_to_artist, 11)

# writeFinalArtists(artists_final)

