import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Spotify Recommendation",
    page_icon =":🎧",
    layout="wide"
)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_codings = load_lottieurl("https://lottie.host/6907dce6-3b9d-4197-a7fc-03c6c6a6b82a/IiOvEnY07N.json")

# Header section  
with st.container():
   st.subheader("Listen songs only you like 🎶", )
   st.title("Spotify Recommendation 🤔")
   st.write("Recommendations based on liked🙂 and disliked🙃 songs")
 
with st.container():
    left_columns, right_columns = st.columns(2)
        
with right_columns:
    st_lottie(lottie_codings, height=300)
 
 
if st.button("Start Predicting"):
    switch_page ("Predict")