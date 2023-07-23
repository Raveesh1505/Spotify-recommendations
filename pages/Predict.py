import requests
import streamlit as st
from streamlit_lottie import st_lottie


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

# -----------load assets------
lottie_codings = load_lottieurl("https://lottie.host/82cb219c-5702-404f-9216-e10ccd69189b/P8c0A6vm19.json")



with st.container():
    left_columns, right_columns = st.columns(2)
    
with left_columns:
    st_lottie(lottie_codings, height=300)

txt = st.text_input(
    label = "Enter song name 🎶", 
    max_chars = 50, 
    placeholder = "Song here"
)
st.write(txt)

txt2 = st.text_input(
    label= "Enter artist name 🧑‍🎤",
    max_chars = 30,
    placeholder = "name here"
)
