"""
Script file will congest and simplify all the functions that will be used
in the web app in order to get the predictions
"""

# Importing libraries
import os
from dotenv import load_dotenv, find_dotenv
import base64
import requests
import pandas as pd

# Loading env variables
load_dotenv(find_dotenv())
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Function to get spotify token
def getToken():
    authString  = f"{CLIENT_ID}:{CLIENT_SECRET}"
    authBytes   = authString.encode("utf-8")
    authBase64  = str(base64.b64encode(authBytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    tokenHeaders = {
        "Authorization" : f"Basic {authBase64}",
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    tokenData = {
        "grant_type" : "client_credentials"
    }
    tokenResponse = requests.post(
        url,
        headers=tokenHeaders,
        data=tokenData
    )
    tokenData   = tokenResponse.json()
    TOKEN       = tokenData['access_token']
    return TOKEN

# Function to get song ID
def getTrack(token, song_name, artist_name):
    url         = "https://api.spotify.com/v1/search"
    query       = f"?q=track:{song_name}%20artist:{artist_name}&type=track&limit=1"
    queryURL    = url+query
    songHeaders = {
        "Authorization" : f"Bearer {token}"
    }
    songResponse = requests.get(
        queryURL,
        headers=songHeaders
    )
    songData = songResponse.json()
    songDF   = pd.json_normalize(songData['tracks'], record_path='items')
    if len(songDF) > 0:
        ID = songDF['id'].iloc[0]
        songURI = songDF['uri'].iloc[0]
        songURI = songURI.split(':')[2]
        return ID, songURI
    else:
        return False

# Function to get song features
def getSongFeatures(token, songID):
    url = f'https://api.spotify.com/v1/audio-features?ids={songID}'
    songFeaturesHeaders = {
        "Authorization" : f"Bearer {token}"
    }
    featureResponse = requests.get(
        url,
        headers=songFeaturesHeaders
    )
    data    = featureResponse.json()
    dataDF  = pd.json_normalize(data['audio_features'])
    dataDF  = dataDF[['time_signature', 'danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'loudness', 'tempo', 'duration_ms']]
    return dataDF

# Function to get prediction
def predictionModel(data, songPredictionModel):
    prediction = songPredictionModel.predict(data)
    return prediction

# Final function to predict song cluster
def predictSong(songPredictionModel, songName, artistName):
    TOKEN   = getToken()
    songData  = getTrack(TOKEN, songName, artistName)
    if songData:
        songID, songURI = songData
        songFeaturesData = getSongFeatures(TOKEN, songID)
        prediction = predictionModel(songFeaturesData, songPredictionModel)
        return prediction
    else:
        return None

# Function to return related songs
def getRelevantSongs(clusterNumber):
    predictedData = pd.read_csv('/Users/raveeshyadav/GitHub/Spotify-recommendations/songs/predictionData.csv', index_col=0)
    # Cleaning the data
    listenNowURL = []
    for row in range (0, len(predictedData)):
        listenNowURL.append('https://open.spotify.com/track/{}'.format(predictedData['id'][row]))
    predictedData['Listen Now'] = listenNowURL
    predictedData = predictedData[predictedData['cluster'] == clusterNumber]
    return predictedData.drop(columns=['id', 'cluster'])