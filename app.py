"""
Web App for Spotify Recommendations
"""

# Importing libraries
import streamlit as st
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
import os
from dotenv import load_dotenv, find_dotenv
import base64
import requests
import pandas as pd

# Creating a spark session
spark = SparkSession.builder.master("local[2]").appName("Spotify_Recommendations").getOrCreate()

# Loading the prediction model
songPredictionModel = LogisticRegressionModel.load("songPredictionModel")

# Loading env variables
load_dotenv(find_dotenv())
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Method to get spotify token
def getToken():
    authString = f"{CLIENT_ID}:{CLIENT_SECRET}"
    authBytes = authString.encode("utf-8")
    authBase64 = str(base64.b64encode(authBytes), "utf-8")

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
    tokenData = tokenResponse.json()
    TOKEN = tokenData['access_token']
    return TOKEN

# Method to get song ID
def getTrack(token, song_name, artist_name):
    url = "https://api.spotify.com/v1/search"
    query = f"?q=track:{song_name}%20artist:{artist_name}&type=track&limit=1"
    queryURL = url+query
    songHeaders = {
        "Authorization" : f"Bearer {token}"
    }
    songResponse = requests.get(
        queryURL,
        headers=songHeaders
    )
    songData = songResponse.json()
    songDF = pd.json_normalize(songData['tracks'], record_path='items')
    ID = songDF['id'].iloc[0]
    return ID

# Method to get song features
def getSongFeatures(token, songID):
    url = f'https://api.spotify.com/v1/audio-features?ids={songID}'
    songFeaturesHeaders = {
        "Authorization" : f"Bearer {token}"
    }
    featureResponse = requests.get(
        url,
        headers=songFeaturesHeaders
    )
    data = featureResponse.json()
    dataDF = pd.json_normalize(data['audio_features'])
    dataDF = dataDF.iloc[:, :11]
    dataRaw = spark.createDataFrame(dataDF)
    return dataRaw

# Method to get prediction
def predictionModel(features, songPredictionModel):
    feature_names = features.columns[:]
    assembler = VectorAssembler(inputCols=feature_names, outputCol="features")
    testingData = assembler.transform(features)
    predictionDF = songPredictionModel.transform(testingData)
    prediction = predictionDF.first()["prediction"]
    return prediction

# Final method
def predictSong(songPredictionModel, song_name, artist_name):
    TOKEN = getToken()
    songID = getTrack(TOKEN, song_name, artist_name)
    rawSongFeatures = getSongFeatures(TOKEN, songID)
    prediction = predictionModel(rawSongFeatures, songPredictionModel)
    return prediction

#
#
#
#
#
#
#
#

# Streamlit ap design
# title - SPOTIFY RECOMMENDATIONS
# button - START PREDICTING
# When we click this button - it will start a new form
# Form details:
# Enter song name: 
# Enter artist name: 
# Button - predict
# When we click this button - it will show the result

if st.button("PREDICT"):
    predictionOutput = predictSong()