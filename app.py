import streamlit as st

st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="🎥"
)

st.title("🎥 YouTube Video Summarizer")

url = st.text_input("Enter YouTube URL")

if st.button("Summarize"):
    st.write("Processing...")
    