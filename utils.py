from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables
load_dotenv()


# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# -----------------------------------
# Extract YouTube Video ID
# -----------------------------------

def extract_video_id(url):

    parsed_url = urlparse(url)

    # Normal YouTube URL
    if "youtube.com" in parsed_url.netloc:

        video_ids = parse_qs(parsed_url.query).get("v")

        if not video_ids:
            raise ValueError("YouTube video ID not found.")

        return video_ids[0]

    # Short YouTube URL
    elif "youtu.be" in parsed_url.netloc:

        video_id = parsed_url.path.strip("/")

        if not video_id:
            raise ValueError("YouTube video ID not found.")

        return video_id.split("/")[0]

    else:
        raise ValueError("Please enter a valid YouTube URL.")


# -----------------------------------
# Get YouTube Transcript
# -----------------------------------

def get_transcript(video_id):

    api = YouTubeTranscriptApi()

    # Get all available transcripts
    transcript_list = api.list(video_id)

    # First try Hindi
    try:
        transcript = transcript_list.find_transcript(["hi"])

    except Exception:

        # If Hindi is not available, try English
        try:
            transcript = transcript_list.find_transcript(["en"])

        except Exception:

            # If neither is available
            raise ValueError(
                "No Hindi or English transcript is available for this video."
            )

    # Fetch transcript
    transcript_data = transcript.fetch()

    # Convert transcript into one large text
    text_parts = []

    for item in transcript_data:
        text_parts.append(item.text)

    return " ".join(text_parts)


# -----------------------------------
# Basic Gemini Summary
# -----------------------------------

def summarize_text(transcript):

    prompt = f"""
You are an expert YouTube video summarizer.

Summarize the following YouTube transcript
in simple and clear language.

Give the answer in this format:

## Summary
Write a clear summary of the video.

## Key Points
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

## Important Takeaways
- Takeaway 1
- Takeaway 2
- Takeaway 3

Transcript:

{transcript}
"""

    response = llm.invoke(prompt)

    return response.content