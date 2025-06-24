def save_to_csv(df, filename="combined_channel_videos.csv"):
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} videos from {df['Channel ID'].nunique()} channels to '{filename}'")

