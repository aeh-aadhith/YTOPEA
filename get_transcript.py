from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def videoID_to_transcript(video_id, language='en'):
    """
    Fetch transcript entries for a given video ID and language.
    Returns a list of text entries or None.
    """
    try:
        entries = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        if entries:
            transcript = " ".join([entry['text'] for entry in entries])
        return transcript
    
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for video ID: {video_id}")
    except NoTranscriptFound:
        print(f"No transcript found in '{language}' for video ID: {video_id}")
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
    return None

# ---------- Example Usage ---------- #
if __name__ == "__main__":
    video_id = "umFJaBv2O9U"
    transcript = videoID_to_transcript(video_id)
    
    if transcript:
        print("Transcript:\n")
        print(transcript)
    else:
        print("Transcript not available.")
