import google.generativeai as genai
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key='AIzaSyDE07FXFw-HpOvcwVXSX6V424ETcr75ls0')


def extract_video_transcript(video_url):
    video_id = video_url.split("v=")[1]

    ydl_opts = {
        'quiet': True,
        'skip_download': True, 
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', 'No title found')
        except Exception as e:
            video_title = f"An error occurred while fetching title: {str(e)}"

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = "\n".join([entry['text'] for entry in transcript])
    except Exception as e:
        transcript_text = f"An error occurred while fetching transcript: {
            str(e)}"

    return video_title, transcript_text


def generate_summary(youtube_url, word_count):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        video_title, transcript = extract_video_transcript(youtube_url)
        if "Error" in transcript:
            return video_title, "Could not retrieve transcript for the video."

        prompt = f"""
                Summarize the following YouTube video transcript into approximately {word_count} words:
                Transcript: {transcript}
                """

        response = model.generate_content(prompt)

        if response and hasattr(response, 'candidates') and response.candidates:
            summary = response.candidates[0].content.parts[0].text.strip()
            print(summary)

        return video_title, summary

    except Exception as e:
        return "Error processing video", f"An error occurred: {str(e)}"
