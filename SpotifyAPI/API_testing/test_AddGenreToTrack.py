import requests
from time import sleep
import json
import pandas as pd

# Load chart data
chart = pd.read_csv('regional-gb-weekly-2024-01-04.csv')
track_details = chart[['track_name', 'artist_names']]

# Load Spotify token
with open('spotify_access_token.json', 'r') as file:
    token_data = json.load(file)
access_token = token_data['access_token']
headers = {'Authorization': f'Bearer {access_token}'}

# Last.fm API key
LASTFM_API_KEY = '1248d8056afa6877059f8441e116e073'

# Initialize result lists
# Build a list of dictionaries containing {'artist': artist_name, 'song_name': song_name, 'genre': genre}
AudioDB_genre_list = []
SpotifyAPI_genre_list = []
LastFM_genre_list = []

# Loop through all track to request genre for all
for track_n in range(len(track_details)):
    song_name,artist = track_details.iloc[track_n,:]

    # Make request to AudioDB
    audioDB_endpoint = f'https://www.theaudiodb.com/api/v1/json/523532/searchtrack.php?s={artist}&t={song_name}'
    request = requests.get(audioDB_endpoint)
    audioDB_data = request.json()

    # Make request to SpotifyAPI
    spotify_endpoint = f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1"
    request = requests.get(spotify_endpoint, headers=headers)
    if request.status_code == 401: # Check the token hasn't expired
        raise Exception(f'Spotify token expired, please rerun spotify_connection.py: Status code:{request.status_code}')
    spotify_data = request.json()

    # ------------------ Last.fm API ------------------
    lastfm_endpoint = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'track.getInfo',
        'api_key': LASTFM_API_KEY,
        'artist': artist,
        'track': song_name,
        'format': 'json'
    }
    try:
        response = requests.get(lastfm_endpoint, params=params)
        data = response.json()
        genre = data['track']['toptags']['tag'][0]['name']
        LastFM_genre_list.append({'artist': artist, 'song_name': song_name, 'genre': genre})
    except Exception:
        LastFM_genre_list.append({'artist': artist, 'song_name': song_name, 'genre': None})

    # Save Spotify data
    try:
        genre = spotify_data['artists']['items'][0]['genres'][0]
        SpotifyAPI_genre_list += [{'artist':artist,'song_name':song_name,'genre':genre}]
    except Exception:
        SpotifyAPI_genre_list += [{'artist':artist,'song_name':song_name,'genre':None}]

    # Save audioDB data
    try:
        genre = audioDB_data['track'][0]['strGenre']
        AudioDB_genre_list += [{'artist':artist,'song_name':song_name,'genre':genre}]
    except Exception:
        AudioDB_genre_list += [{'artist':artist,'song_name':song_name,'genre':None}]

    finally:
        sleep(0.5) # Maximum 2 calls per second on AudioDB API methods


# Save all outputs
with open('test_AudioDB_genres.json', 'w') as file:
    json.dump(AudioDB_genre_list, file, indent=2)

with open('test_Spotify_genres.json', 'w') as file:
    json.dump(SpotifyAPI_genre_list, file, indent=2)

with open('test_LastFM_genres.json', 'w') as file:
    json.dump(LastFM_genre_list, file, indent=2)







