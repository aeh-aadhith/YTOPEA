import video_data_extraction
from get_transcript import videoID_to_transcript
import LLM_Classfn
from tools import save_to_csv

if __name__ == "__main__":

    example_channel_id = [
        'UCfBf_eZSur4tGh-uSuqXZoA',
        'UCuyl9HIbX_fYTuJbLEz1KQw'
    ]
    
    df = video_data_extraction.many_channels(example_channel_id)

    classifications = []
    transcripts_available = []

    for idx, row in df.iterrows():
        video_id = row["Video ID"]
        title = row["Title"]
        description = row["Description"]
        label = None

        transcript = videoID_to_transcript(video_id)

        if transcript:
            transcripts_available.append("Yes")
        else:
            transcripts_available.append("No")

        # Option 1: Classify video even without transcript
        label = LLM_Classfn.classify_video(title=title, description=description, transcript=transcript)
        
        # Option 2: Classify only if there is transcript
        # if transcript:
        #     label = LLM_Classfn.classify_ophthalmology_video_with_title(title=title, description=description)
        # else:
        #     label = None  

        print(f"{video_id} → {label}")
        classifications.append(label)
    
    df['Transcript_Available'] = transcripts_available
    df["Classification"] = classifications
    save_to_csv(df)