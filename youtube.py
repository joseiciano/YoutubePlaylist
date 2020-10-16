import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("API_KEY")

youtube = build('youtube', 'v3', developerKey=API_KEY)

url_link = 'https://www.youtube.com/playlist?list=PL4AWxkId50utoYIbd64M7E1IzTu6ZYadt'
playlist_id = url_link.split('=')[1]

# Get playlist name
request = youtube.playlists().list(
    part='snippet',
    id=playlist_id
)

response = request.execute()
playlist_name = response['items'][0]['snippet']['localized']['title']
playlist_name = playlist_name.replace(' ', '_')

# Generate request body
request = youtube.playlistItems().list(
    part='snippet',
    playlistId=playlist_id
)

# Make request
response = request.execute()

videos = []

while response:
    for item in response['items']:
        videos.append({
            'title': item['snippet']['title'],
            'channel_id': item['snippet']['channelId'],
            'published_at': item['snippet']['publishedAt'],
            'video_id': item['snippet']['resourceId']['videoId']
        })

    request = youtube.playlistItems().list(
        part='snippet',
        playlistId='PL4AWxkId50utoYIbd64M7E1IzTu6ZYadt',
        pageToken=response.get('nextPageToken', None)
    )

json_string = json.dumps(videos, indent=4)
with open(f'{playlist_name}.json', 'w') as f:
    f.write(json_string)
