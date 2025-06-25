def save_to_csv(df, filename="combined_channel_videos.csv"):
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} videos from {df['Channel ID'].nunique()} channels to '{filename}'")

def shorten_transcript(transcript: str, max_tokens: int = 4500) -> str:
    """
    Iteratively trims the transcript to stay under token limits by cutting the middle.
    Keeps the start and end intact, discards the middle until under limit.
    """

    max_chars = max_tokens * 4  # Let's assume 4 characters = 1 token on average
    omitted_notice = "\n... [middle omitted due to length] ...\n"
    
    while len(transcript) > max_chars:
        keep_chars = (max_chars - len(omitted_notice)) // 2
        start_chunk = transcript[:keep_chars]
        end_chunk = transcript[-keep_chars:]
        transcript = start_chunk + omitted_notice + end_chunk
    
    return transcript