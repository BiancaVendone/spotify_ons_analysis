import requests
from pprint import pprint

'''
Wrote code using info on: https://www.last.fm/api/show/artist.getInfo
'''

# Query details
API_KEY = '1248d8056afa6877059f8441e116e073'
ARTIST = 'Bad Bunny'  # change this if you know the correct artist
TRACK = 'DtMF'

# Build Last.fm request
lastfm_endpoint = 'http://ws.audioscrobbler.com/2.0/'

params = {
    'method': 'track.getInfo',
    'api_key': API_KEY,
    'artist': ARTIST,
    'track': TRACK,
    'format': 'json'
}

# Make request
response = requests.get(lastfm_endpoint, params=params)
data = response.json()

pprint(data)


#Extract genres (tags)
if 'track' in data and 'toptags' in data['track']:
    tags = data['track']['toptags'].get('tag', [])
    genre_list = [tag['name'] for tag in tags]

    print(f"Genres (tags) for '{TRACK}' by {ARTIST}:")
    print(genre_list)
else:
    print("No genre data found for this track.")
