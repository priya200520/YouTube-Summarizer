import streamlit as st

from utils import extract_video_id, get_transcript
from summarizer import (
    split_transcript,
    summarize_chunks,
    create_final_summary
)

st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="🎥"
)

st.title("🎥 YouTube Video Summarizer")

url = st.text_input("Enter YouTube URL")

if st.button("Summarize"):

    if not url:
        st.warning("Please enter a YouTube URL.")

    else:
        try:
            video_id = extract_video_id(url)

            with st.spinner("Getting transcript..."):
                transcript = get_transcript(video_id)

            st.success("Transcript fetched successfully!")

            with st.spinner("Splitting transcript into chunks..."):
                chunks = split_transcript(transcript)

            st.write("Total Chunks:", len(chunks))

            with st.spinner("Generating summaries..."):
                summaries = summarize_chunks(chunks)

            with st.spinner("Creating final summary..."):
                final_summary = create_final_summary(summaries)

            st.success("Summary Generated!")

            st.markdown(final_summary)

        except Exception as e:
            st.error(f"Error: {e}")
