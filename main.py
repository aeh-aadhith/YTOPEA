import video_data_extraction
from get_transcript import videoID_to_transcript
import LLM_Classfn
from tools import save_to_csv, shorten_transcript
import pandas as pd

if __name__ == "__main__":

    example_channel_id = [
        'UCuyl9HIbX_fYTuJbLEz1KQw'
    ]
    import os

    output_path = "Aurotube_videos.csv"

    # Load previous progress if file exists
    if os.path.exists(output_path):
        df = pd.read_csv(output_path)
        start_index = len(df)
        print(f"Resuming from index {start_index} (already classified: {start_index})")
    else:
        df = video_data_extraction.many_channels(example_channel_id)
        df["Transcript_Available"] = ""
        df["Classification"] = ""
        start_index = 0

    for idx in range(start_index, len(df)):
        row = df.loc[idx]
        video_id = row["Video ID"]
        title = row["Title"]
        description = row["Description"]
        transcript = videoID_to_transcript(video_id)

        if transcript:
            transcript = shorten_transcript(transcript)
            df.at[idx, 'Transcript_Available'] = "Yes"
        else:
            df.at[idx, 'Transcript_Available'] = "No"

        try:
            label = LLM_Classfn.classify_video(title=title, description=description, transcript=transcript)
        except Exception as e:
            print(f"Error classifying {video_id}: {e}")
            label = None

        df.at[idx, "Classification"] = label
        print(f"{video_id} → {label}")

        df.to_csv(output_path, index=False)