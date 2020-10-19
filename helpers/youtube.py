import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_playlist_name(playlist_id):
    '''
        Searches for and returns the name of playlist passed
    '''
    # Generate request
    request = youtube.playlists().list(
        part='snippet',
        id=playlist_id
    )
    response = request.execute()

    # Obtain playlist name, remove whitespace just for readability
    playlist_name = response['items'][0]['snippet']['localized']['title']
    playlist_name = playlist_name.replace(' ', '_')
    return playlist_name


def get_playlist_info(playlist_id):
    '''
        Obtains information about the passed in playlist. 
        Returns an dictionary of objects containing: title, channel, publish date, and videoid
    '''

    # Generate request body
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id
    )
    response = request.execute()

    # Dictionary of objects detailing videos in playlist
    videos = {}

    # Sift through responses
    while response:
        # For each video in the playlist add it to videos dict
        for item in response['items']:
            title = item['snippet']['title']
            channel_id = item['snippet']['channelId']
            published_at = item['snippet']['publishedAt']
            video_id = item['snippet']['resourceId']['videoId']

            videos[video_id] = {
                'title': title,
                'channel_id': channel_id,
                'published_at': published_at,
                'video_id': video_id
            }

        # Check if there's a next page to sift through
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId='PL4AWxkId50utoYIbd64M7E1IzTu6ZYadt',
            pageToken=response.get('nextPageToken', None)
        )
        response = request.execute()
        break

    return videos
