"""
Script file will congest and simplify all the functions that will be used
in the web app in order to get the predictions
"""

# Importing libraries
from pyspark.ml.feature import VectorAssembler
import os
from dotenv import load_dotenv, find_dotenv
import base64
import requests
import pandas as pd

# Loading env variables
load_dotenv(find_dotenv())
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Method to get spotify token
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

# Method to get song ID
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

# Method to get song features
def getSongFeatures(token, sparkSession, songID):
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
    dataDF  = dataDF.iloc[:, :11]
    dataRaw = sparkSession.createDataFrame(dataDF)
    return dataRaw

# Method to get prediction
def predictionModel(features, songPredictionModel):
    feature_names   = features.columns[:]
    assembler       = VectorAssembler(inputCols=feature_names, outputCol="features")
    testingData     = assembler.transform(features)
    predictionDF    = songPredictionModel.transform(testingData)
    prediction      = predictionDF.first()["prediction"]
    return prediction

# Final method
def predictSong(songPredictionModel, sparkSession, songName, artistName):
    TOKEN   = getToken()
    songData  = getTrack(TOKEN, songName, artistName)
    if songData:
        songID, songURI = songData
        rawSongFeatures = getSongFeatures(TOKEN, sparkSession, songID)
        prediction = predictionModel(rawSongFeatures, songPredictionModel)
        if prediction == 1: 
            prediction = "A" 
        else:
            prediction = "B"
        return (prediction, songURI)
    else:
        return False