import streamlit as st
from urllib.parse import urlparse, parse_qs

from utils import extract_video_id, get_transcript
from summarizer import (
    split_transcript,
    summarize_chunks,
    create_final_summary
)


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="YouTube AI Summarizer",
    page_icon="🎥",
    layout="centered"
)


# -----------------------------------
# Header
# -----------------------------------

st.title("🎥 YouTube AI Summarizer")

st.write(
    "Convert a YouTube video transcript into a clear "
    "AI-powered summary."
)

st.divider()


# -----------------------------------
# YouTube URL
# -----------------------------------

st.subheader("🔗 Enter YouTube Video")

url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


# -----------------------------------
# Video Preview
# -----------------------------------

if url.strip():

    try:

        parsed_url = urlparse(url)

        video_id = None

        # Normal YouTube URL
        if "youtube.com" in parsed_url.netloc:

            video_ids = parse_qs(
                parsed_url.query
            ).get("v")

            if video_ids:
                video_id = video_ids[0]

        # Short YouTube URL
        elif "youtu.be" in parsed_url.netloc:

            video_id = parsed_url.path.strip(
                "/"
            ).split("/")[0]

        # Show Preview
        if video_id:

            st.subheader("🎬 Video Preview")

            thumbnail_url = (
                f"https://img.youtube.com/vi/"
                f"{video_id}/maxresdefault.jpg"
            )

            st.image(
                thumbnail_url,
                use_container_width=True
            )

            st.markdown(
                f"[▶️ Watch this video on YouTube]"
                f"(https://www.youtube.com/watch?v={video_id})"
            )

    except Exception:
        pass


# -----------------------------------
# Manual Transcript
# -----------------------------------

st.subheader("📝 Or Paste Transcript")

manual_transcript = st.text_area(
    "Paste your transcript here if YouTube "
    "transcript cannot be fetched.",
    height=180
)


# -----------------------------------
# Generate Summary
# -----------------------------------

if st.button(
    "🚀 Generate Summary",
    use_container_width=True
):

    transcript = ""

    try:

        # -----------------------------------
        # Manual Transcript
        # -----------------------------------

        if manual_transcript.strip():

            transcript = manual_transcript

            st.success(
                "✅ Manual transcript received!"
            )


        # -----------------------------------
        # YouTube Transcript
        # -----------------------------------

        elif url.strip():

            with st.spinner(
                "🔍 Fetching YouTube transcript..."
            ):

                video_id = extract_video_id(url)

                transcript = get_transcript(
                    video_id
                )

            st.success(
                "✅ YouTube transcript fetched successfully!"
            )


        # -----------------------------------
        # No Input
        # -----------------------------------

        else:

            st.warning(
                "Please enter a YouTube URL "
                "or paste a transcript."
            )

            st.stop()


        # -----------------------------------
        # Text Splitting
        # -----------------------------------

        with st.spinner(
            "✂️ Splitting transcript into chunks..."
        ):

            chunks = split_transcript(
                transcript
            )

        st.info(
            f"📦 Transcript divided into "
            f"{len(chunks)} chunks."
        )


        # -----------------------------------
        # Chunk Summaries
        # -----------------------------------

        with st.spinner(
            "🧠 AI is analyzing the video..."
        ):

            summaries = summarize_chunks(
                chunks
            )


        # -----------------------------------
        # Final Summary
        # -----------------------------------

        with st.spinner(
            "📝 Creating final summary..."
        ):

            final_summary = create_final_summary(
                summaries
            )


        # -----------------------------------
        # Display Summary
        # -----------------------------------

        st.divider()

        st.subheader(
            "📑 AI Generated Summary"
        )

        st.markdown(
            final_summary
        )


        # -----------------------------------
        # Download Summary
        # -----------------------------------

        st.download_button(
            label="📥 Download Summary",
            data=final_summary,
            file_name="youtube_summary.txt",
            mime="text/plain",
            use_container_width=True
        )


    except Exception as e:

        st.error(
            f"❌ Error: {e}"
        )


# -----------------------------------
# Footer
# -----------------------------------

st.divider()

st.caption(
    "Built with Python • LangChain • Gemini • Streamlit"
)