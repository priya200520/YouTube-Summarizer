import streamlit as st
from utils import extract_video_id, get_transcript

st.title("🎥 YouTube Video Summarizer")

url = st.text_input("Enter YouTube URL")

if st.button("Get Transcript"):

    video_id = extract_video_id(url)

    transcript = get_transcript(video_id)

    st.write(transcript[:1000])