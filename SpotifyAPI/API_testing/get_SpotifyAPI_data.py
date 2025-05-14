import json
import requests

# GET TOKEN
with open('spotify_access_token.json', 'r') as file:
    token_data = json.load(file)

access_token = token_data['access_token']

# Set token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# EXAMPLE FOR GETTING GENRE FOR SPECIFIC TRACK
# 1. Search for the track to get artist ID
track_title = "DtMF"
search_track_url = f"https://api.spotify.com/v1/search?q={track_title}&type=track&limit=1"
search_track_response = requests.get(search_track_url, headers=headers).json()

# Get the first track's artist ID
artist_id = search_track_response['tracks']['items'][0]['artists'][0]['id']
print(f'This is the artist_id: {artist_id}')

# 2. Get genres from artist
artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
artist_response = requests.get(artist_url, headers=headers).json()
print(f"This is the artist's json response:\n {artist_response}")

genres = artist_response['genres']
print(f"Genres for '{track_title}':", genres)
