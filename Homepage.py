"""
HOMEPAGE is the main python script for web app. This is the script for
homepage of app as the name suggests.
"""

# Importing libraries
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page

# Base page configs
st.set_page_config(
    page_title="Spotify Recommendation",
    page_icon =":🎧",
    layout="wide"
)

st.write("Search and predict songs based on your taste!")
st.title("Spotify Recommendation 🤔")
st.subheader("Search and predict songs based on your taste!")
leftColumn, rightColumn = st.columns(2)

# Creating lottie function which will help in posting
# stickers on the webpage for better looks.
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Calling the sticker
lottieBoy = load_lottieurl("https://lottie.host/6907dce6-3b9d-4197-a7fc-03c6c6a6b82a/IiOvEnY07N.json")
lottiePredict = load_lottieurl("https://lottie.host/9adcaff5-47d2-46da-946d-777160241ca3/pnYOqlGbof.json")
lottieSearch = load_lottieurl("https://lottie.host/9103b5c4-d70b-4679-a369-f995c2014b7b/1Ru8qyXAcv.json")
lottieInfo = load_lottieurl("https://lottie.host/4ca73eb6-3090-4306-af4e-7d78578a7707/MfNe8fKb2G.json")

# Differentiating the page into left and right containers
# for easy and neater placement of elements  

with rightColumn:
    st_lottie(lottieBoy, height=300)

with leftColumn: 
    col1, col2, col3 = st.columns(3)
    # Button to take the user to prediction page
    with col1:
        st_lottie(lottiePredict) 
        if st.button("Start Predicting"):
            switch_page("Predict")
    with col2:
        st_lottie(lottieSearch)
        if st.button("Search Songs"):
            switch_page("Search")
    with col3:
        st_lottie(lottieInfo)
        if st.button("About the app"):
            switch_page("Info")