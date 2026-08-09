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

st.write("YouTube video ka URL enter karo ya transcript manually paste karo.")

# YouTube URL
url = st.text_input("🔗 YouTube URL")

# Manual transcript
manual_transcript = st.text_area(
    "📝 Agar YouTube transcript fetch na ho, transcript yahan paste karo:",
    height=200
)


if st.button("Summarize"):

    transcript = ""

    try:

        # Manual transcript has priority
        if manual_transcript.strip():

            transcript = manual_transcript

            st.success("Manual transcript received!")

        # Otherwise get transcript from YouTube
        elif url.strip():

            with st.spinner("Getting YouTube transcript..."):

                video_id = extract_video_id(url)

                transcript = get_transcript(video_id)

            st.success("YouTube transcript fetched successfully!")

        else:

            st.warning(
                "Please enter a YouTube URL or paste a transcript."
            )

            st.stop()


        # Split transcript
        with st.spinner("Splitting transcript into chunks..."):

            chunks = split_transcript(transcript)

        st.info(f"Transcript divided into {len(chunks)} chunks.")


        # Summarize chunks
        with st.spinner("Generating AI summaries..."):

            summaries = summarize_chunks(chunks)


        # Final summary
        with st.spinner("Creating final summary..."):

            final_summary = create_final_summary(summaries)


        st.success("🎉 Summary Generated!")

        st.markdown(final_summary)


    except Exception as e:

        st.error(f"Error: {e}")