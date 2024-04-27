"""
PREDICTION PAGE

This is the script for page on web app that will take 
user input and predict if the user will like or dilike
the entered song.
"""

# Importing libraries
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
import joblib
from script import predictSong
from sklearn.preprocessing import StandardScaler

# Base page configs
st.set_page_config(
    page_title="Spotify Recommendation",
    page_icon =":🎧",
    layout="wide"
)

@st.cache_resource()
# Loading the model
def loadModel():
    songPredictionModel = joblib.load("/Users/raveeshyadav/GitHub/Spotify-recommendations/songs_prediction_model.pkl")
    return songPredictionModel

songPredictionModel = loadModel()

# Creating a standard scalar
standScalar = StandardScaler() 

st.title("Predict Song")

# Creating lottie function which will help in posting
# stickers on the webpage for better looks.
def load_lottieurl(url):
    result = requests.get(url)
    if result.status_code != 200:
        return None
    return result.json()

# Calling the sticker
lottie_codings = load_lottieurl("https://lottie.host/82cb219c-5702-404f-9216-e10ccd69189b/P8c0A6vm19.json")

# Differentiating the page into left and right containers
# for easy and neater placement of elements 
with st.container():
    upCotainer, downContainer = st.columns(2)
    
with upCotainer:
    st_lottie(lottie_codings, height=300)

# Taking user input for the song name
songName = st.text_input(
    label = "Enter song name 🎶", 
    max_chars = 50, 
    placeholder = "Song here"
)

# Taking user input for artist name
artistName = st.text_input(
    label= "Enter artist name 🧑‍🎤",
    max_chars = 30,
    placeholder = "name here"
)

# Predict button will show the result predicted by the model
if st.button("Predict"):
    songData = predictSong(songPredictionModel, songName, artistName, standScalar)
    if songData:
        songPrediction, songURI = songData
        embedLink = f'https://open.spotify.com/embed/track/{songURI}'
        if songPrediction == "B":
            st.error('Hmmm! Through our predictions it looks like will NOT ENJOY this song. However you may try it below!')
            components.iframe(embedLink, height=300)
        else:
            st.success('Through our predictions, it looks like you will ENJOY this song!! Enjoy listening to it below')
            st.balloons()
            components.iframe(embedLink, height=300)
    else:
        st.error("That's strange! The song you entered is not available. Please try again with another song.")