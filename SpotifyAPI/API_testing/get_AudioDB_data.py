import requests


'''
Return track details from artist/track name
searchtrack.php?s={Artist_Name}&t={Single_Name}
Example - www.theaudiodb.com/api/v1/json/{APIKEY}/searchtrack.php?s=coldplay&t=yellow '''

# Build endpoint
title = 'DtMF'
artist = 'Bad Bunny'
audioDB_endpoint = f'https://www.theaudiodb.com/api/v1/json/523532/searchtrack.php?s={artist}&t={title}'

# Make request
response = requests.get(audioDB_endpoint)
data = response.json()

try:
    genre = data['track'][0]['strGenre']

    print(f"Genres (tags) for '{title}' by {artist}:")
    print(genre,)
except Exception as e:
    print(f"No genre data found for this track. {e}")
