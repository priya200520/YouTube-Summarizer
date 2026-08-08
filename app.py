import streamlit as st
from utils import extract_video_id, get_transcript, summarize_text

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
            with st.spinner("Getting transcript..."):
                video_id = extract_video_id(url)
                transcript = get_transcript(video_id)

            st.success("Transcript fetched successfully!")

            with st.spinner("Generating AI summary..."):
                summary = summarize_text(transcript)

            st.subheader("📝 AI Summary")
            st.markdown(summary)

        except Exception as e:
            st.error(f"Error: {e}")