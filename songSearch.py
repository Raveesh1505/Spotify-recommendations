import pandas as pd
import requests

def getArtist(token, artistName):
    """
    Function to get artist id and it's genres.
    Returns list of list of genres and ID.
    """
    url = "https://api.spotify.com/v1/search"
    query = f"?q=artist:{artistName}&type=artist&limit=1"
    queryURL = url+query
    artistHeaders = {
        "Authorization" : f"Bearer {token}"
    }
    artistResponse = requests.get(
        queryURL,
        headers=artistHeaders
    )
    artistData = artistResponse.json()
    artistDF = pd.json_normalize(artistData['artists'], record_path='items')
    if len(artistDF) > 0:    
        return artistDF['id'].iloc[0]
    else:
        return False

def songSuggestion(token, artistID, artistGenres, songID, limit):
    """
    Song suggestion based on input
    """
    url = "https://api.spotify.com/v1/recommendations"
    mainQuery = f"?seed_artists={artistID}&seed_genres={artistGenres}&seed_tracks={songID}&limit={limit}"
    queryURL = url+mainQuery
    suggestionHeaders = {
        "Authorization" : f"Bearer {token}"
    }
    suggestionResponse = requests.get(
        queryURL,
        headers=suggestionHeaders
    )
    suggestions = suggestionResponse.json()
    suggestionsDF = pd.json_normalize(suggestions['tracks'])
    if len(suggestionsDF) > 0:
        return suggestionsDF['id'].tolist()
    else:
        return False

# Get genres
def getGenres(token):
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    reponse = requests.get(
        url,
        headers=headers
    )
    reponseJSON = reponse.json()
    return list(reponseJSON['genres'])