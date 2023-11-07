# Neccessary modules

import sys
import os
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Spotify API credentials from credentials.txt

with open('credentials.txt') as f:
    credentials = f.readlines()
    credentials = [c.strip() for c in credentials]


# Spotify API credentials and Client ID

client_id = credentials[0]
client_secret = credentials[1]
redirect_uri = credentials[2]


# Spotify API scope

scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative user-read-recently-played user-top-read user-read-playback-position user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-read-email user-read-private'


# Spotify API token

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))


# Get artist ID from artist name

def get_artist_id(artist_name):
    artist = sp.search(q='artist:' + artist_name, type='artist')
    artist_id = artist['artists']['items'][0]['id']
    return artist_id


# Get artist name from artist ID

def get_artist_name(artist_id):
    artist = sp.artist(artist_id)
    artist_name = artist['name']
    return artist_name


# Get all data from artist ID as a dataframe

def get_artist_data(artist_id):
    artist = sp.artist(artist_id)
    artist_name = artist['name']
    artist_genres = artist['genres']
    artist_popularity = artist['popularity']
    artist_followers = artist['followers']['total']
    artist_data = pd.DataFrame({'artist_name': [artist_name], 'artist_genres': [artist_genres], 'artist_popularity': [artist_popularity], 'artist_followers': [artist_followers]})
    return artist_data

def get_artist_albums(artist_id):
    albums = sp.artist_albums(artist_id)
    albums = albums['items']
    album_ids = []
    album_names = []
    album_release_dates = []
    album_total_tracks = []
    for album in albums:
        album_ids.append(album['id'])
        album_names.append(album['name'])
        album_release_dates.append(album['release_date'])
        album_total_tracks.append(album['total_tracks'])
    album_data = pd.DataFrame({'album_id': album_ids, 'album_name': album_names, 'album_release_date': album_release_dates, 'album_total_tracks': album_total_tracks})
    return album_data


# Get album ID from artist name and album name

def get_album_ID(artist_name, album_name):
    album = sp.search(q='album:' + album_name + ' artist:' + artist_name, type='album')
    album_id = album['albums']['items'][0]['id']
    return album_id


# get album data

def get_album_data(album_id):
    album = sp.album(album_id)
    album_name = album['name']
    album_release_date = album['release_date']
    album_total_tracks = album['total_tracks']
    album_data = pd.DataFrame({'album_name': [album_name], 'album_release_date': [album_release_date], 'album_total_tracks': [album_total_tracks]})
    return album_data


# This function takes the album's ID element as a parameter and returns datas about of tracks in a album.
def get_album_tracks_with_features(album_id):
    tracks = sp.album_tracks(album_id)['items']
    
    track_data = []

    for track in tracks:

        audio_features = sp.audio_features(track['uri'])[0]

        track_data.append({
            "name": track['name'],
            "id": track['id'],
            "uri": track['uri'],
            "danceability": audio_features['danceability'],
            "energy": audio_features['energy'],
            "key": audio_features['key'],
            "loudness": audio_features['loudness'],
            "mode": audio_features['mode'],
            "speechiness": audio_features['speechiness'],
            "acousticness": audio_features['acousticness'],
            "instrumentalness": audio_features['instrumentalness'],
            "liveness": audio_features['liveness'],
            "valence": audio_features['valence'],
            "tempo": audio_features['tempo'],
            "duration_ms": audio_features['duration_ms'],
        })

    return pd.DataFrame(track_data)


# Now we try yo get all tracks from an artist using functions above

artist = 'Selah Sue'
artist_id = get_artist_id(artist)
artist_name = get_artist_name(artist_id)
artist_data = get_artist_data(artist_id)
artist_albums = get_artist_albums(artist_id)
artists_albums_ids = artist_albums['album_id'].tolist()

print(artist_name)
print(artist_data)
print(artist_albums)

for i in artists_albums_ids:
    print(get_album_tracks_with_features(i))

# Now we try yo get lyrics of a song using genius API

from lyricsgenius import Genius

genius = Genius('xshAT2hxnblqfWr89MUz5I43cD13tpyMzSoig7lU0axw4QKFjVu-t10QjlViYsYH')

song_title = 'Fyah Fyah'
artist_name = 'Selah Sue'

song = genius.search_song(song_title, artist_name)
print(song.lyrics)

song_2 = 'She and Her Darkness'
artist_2 = 'Diary of Dreams'

song_2 = genius.search_song(song_2, artist_2)
print(song_2.lyrics)


# Now let's add lyrics to our dataframe that we created at get_album_tracks_with_features function

def get_tracks(album_id):
    tracks = sp.album_tracks(album_id)['items']

    track_data = []

    for track in tracks:
        
        audio_features = sp.audio_features(track['uri'])[0]

        track_data.append({
            "name": track['name'],
            "id": track['id'],
            "uri": track['uri'],
            "danceability": audio_features['danceability'],
            "energy": audio_features['energy'],
            "key": audio_features['key'],
            "loudness": audio_features['loudness'],
            "mode": audio_features['mode'],
            "speechiness": audio_features['speechiness'],
            "acousticness": audio_features['acousticness'],
            "instrumentalness": audio_features['instrumentalness'],
            "liveness": audio_features['liveness'],
            "valence": audio_features['valence'],
            "tempo": audio_features['tempo'],
            "duration_ms": audio_features['duration_ms'],
            "lyrics": genius.search_song(track['name'], get_artist_name(artist_id)).lyrics
        })

    return pd.DataFrame(track_data)

u = get_tracks(get_album_ID('Selah Sue', 'Selah Sue'))

# to excel

u.to_excel('Selah Sue.xlsx')
