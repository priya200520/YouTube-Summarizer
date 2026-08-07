from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    video_id = url.split("v=")[1]
    return video_id


def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = ""

    for line in transcript:
        text = text + " " + line["text"]

    return text