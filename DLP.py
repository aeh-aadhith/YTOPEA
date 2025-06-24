import subprocess

def get_auto_transcript_text(video_id, lang='en'):
    """
    Fetches auto-generated subtitles (if available) using yt-dlp and returns as plain text.
    Does not save anything to disk.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    command = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", lang,
        "--skip-download",
        "--sub-format", "vtt",
        "-o", "-",  # Output to stdout
        url
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        vtt_data = result.stdout
        return vtt_to_text_from_string(vtt_data)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to fetch subtitles for {video_id}: {e}")
        return None

def vtt_to_text_from_string(vtt_content):
    """
    Converts VTT subtitle content (as string) to plain text.
    """
    lines = vtt_content.splitlines()
    text = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("WEBVTT") or "-->" in line or line.isdigit():
            continue
        text.append(line)
    return " ".join(text)

transcript = get_auto_transcript_text("yLtyCaEleWQ")
if transcript:
    print("Transcript:\n", transcript)
else:
    print("No auto subtitles available.")