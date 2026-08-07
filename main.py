from youtube_transcript_api import YouTubeTranscriptApi

video_id = input("Enter YouTube Video ID: ")

transcript = YouTubeTranscriptApi.get_transcript(video_id)

for line in transcript[:5]:
    print(line["text"])