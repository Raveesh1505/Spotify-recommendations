"""
Search your song!
"""

import streamlit as st
import streamlit.components.v1 as components
from script import getTrack, getToken
from songSearch import *
token = getToken()

# Setting page config
st.set_page_config(
    page_title="Song Search",
    page_icon=":🎧",
    layout="wide"
)

st.title("Search Song")

# Fetching the song name from user
songName = st.text_input(
    label = "Enter song name 🎶", 
    max_chars = 50, 
    placeholder = "Song here"
)

# Fetching the artist name from user
artistName = st.text_input(
    label= "Enter artist name 🧑‍🎤",
    max_chars = 30,
    placeholder = "name here"
)

#Fetching genre details
genresOption = getGenres(token)

# Fetching the genres from user
selectGenres = st.multiselect(
    label = "You may select upto 3 genres and minimum 1",
    options = genresOption,
    max_selections=3
)

# Fetching limit
limit = st.slider(
    label="How many songs should be displayed?",
    min_value= 1,
    max_value= 5
)

# Fetching artist and song details
artistID = getArtist(token, artistName)
songID = getTrack(token, songName, artistName)


if st.button("Suggest!"):
    if artistID != False:
        if songID != False:
            # Converting the genres and ID into string for API input and getting the song's ID
            selectGenres = ','.join(str(genres) for genres in selectGenres)
            # Final recommendation button
            suggestions = songSuggestion(token, artistID, selectGenres, songID[1], limit)
            st.success("Here are some suggestions! You may start listening to them below only")
            for songID in suggestions:
                emebedLink = f'https://open.spotify.com/embed/track/{songID}'
                components.iframe(emebedLink, height=300)
        else:
            st.error("Uhh ohh! Song not found!")
    else:   
        st.error("Uhh ohh! Artist not found!")