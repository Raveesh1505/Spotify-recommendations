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

# Creating lottie function which will help in posting
# stickers on the webpage for better looks.
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Calling the sticker
lottie_codings = load_lottieurl("https://lottie.host/6907dce6-3b9d-4197-a7fc-03c6c6a6b82a/IiOvEnY07N.json")

# Header section  
with st.container():
   st.subheader("Listen songs only you like 🎶", )
   st.title("Spotify Recommendation 🤔")
   st.write("Recommendations based on liked🙂 and disliked🙃 songs")

# Differentiating the page into left and right containers
# for easy and neater placement of elements  
with st.container():
    left_columns, right_columns = st.columns(2)
        
with right_columns:
    st_lottie(lottie_codings, height=300)
 
# Button to take the user to prediction page
if st.button("Start Predicting"):
    switch_page ("Predict")