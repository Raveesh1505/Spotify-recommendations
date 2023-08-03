"""
Page for model insights
"""

import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Reading dataset
df = pd.read_csv(f"{os.path.dirname(os.getcwd())}/Spotify-recommendations/songs_data.csv", index_col=0)
df = df.dropna()

st.set_page_config(
    page_title="Info",
    page_icon=":🎧",
    layout="wide"
)

st.title("Info Page")

tab1, tab2, tab3 = st.tabs(["Dataset Correlation", "Charts", "Training Dataset"])

with tab1:
    # Tab header
    st.header("Dataset Correlation")
    # Printing the plot
    figure, ax = plt.subplots(figsize=(20,10))
    sns.heatmap(df.corr(), ax=ax, annot=True)
    st.pyplot(figure)
    # Analysis of the plot
    st.subheader("Chart Analysis")
    st.markdown("- **High correlation** can be seen between **Energy-Loudness** and **Danceability-Valence**")
    st.markdown("- **Low correlation** can be seen between **Acousticness-Energy** and **Acounsticness-Loudness**")
    

with tab2:
    st.header("Charts")
    st.markdown("You can select desired columns and visualise the correlation between them below")

    xData = st.selectbox("X Axis : ", df.columns)
    yData = st.selectbox("Y Axis : ", df.columns)

    plotData = [xData, yData]
    fig = px.scatter(df, x=plotData[0], y=plotData[1])
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with tab3:
    # Converting the dataframe to csv for download
    csv = df.to_csv().encode('utf-8')
    # Page layout
    st.header("Training Dataset")
    st.markdown("Dataset used to train the model can be seen below")
    st.write(df)
    # CSV Download
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='training_dataset.csv',
        mime='text/csv',
    )