import os
import pandas as pd
from googleapiclient.discovery import build
from tqdm import tqdm
from keys import API_KEY

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
MAX_RESULTS = 100

def get_youtube_client(api_key=API_KEY):
    """Returns a YouTube API client."""
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)


def get_uploads_playlist_id(youtube, channel_id):
    """Returns the uploads playlist ID of the given channel."""
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_video_ids_from_playlist(youtube, playlist_id):
    """Returns all video IDs from the uploads playlist."""
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=MAX_RESULTS,
            pageToken=next_page_token
        )
        response = request.execute()
        video_ids += [item['contentDetails']['videoId'] for item in response['items']]
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids


def get_video_details(youtube, video_ids, channel_id):
    videos_data = []

    for i in tqdm(range(0, len(video_ids), 50), desc=f"Fetching videos for {channel_id}"):
        request = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids[i:i + 50])
        )
        response = request.execute()

        for item in response['items']:
            snippet = item['snippet']
            stats = item.get('statistics', {})
            videos_data.append({
                'Channel ID': channel_id,
                'Video ID': item['id'],
                'Title': snippet.get('title'),
                'Published At': snippet.get('publishedAt'),
                'Views': int(stats.get('viewCount', 0)),
                'Likes': int(stats.get('likeCount', 0)),
                'Comments': int(stats.get('commentCount', 0)),
                'Description': snippet.get('description')
            })

    return pd.DataFrame(videos_data)

def many_channels(channel_ids):
    youtube = get_youtube_client()
    all_data = pd.DataFrame()

    for channel_id in channel_ids:
        try:
            uploads_playlist_id = get_uploads_playlist_id(youtube, channel_id)
            video_ids = get_video_ids_from_playlist(youtube, uploads_playlist_id)
            video_data_df = get_video_details(youtube, video_ids, channel_id)
            all_data = pd.concat([all_data, video_data_df], ignore_index=True)
        except Exception as e:
            print(f"Failed to process channel {channel_id}: {e}")

    return all_data