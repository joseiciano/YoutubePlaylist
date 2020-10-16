import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

youtube = build('youtube', 'v3', developerKey=API_KEY)

request = youtube.playlistItems().list(
    part='snippet',
    playlistId='PL4AWxkId50utoYIbd64M7E1IzTu6ZYadt'
)

response = request.execute()

videos = []

# print(id_response["items"])
# print(id_response["items"][0]['id'])
for item in response['items']:
    print(item['snippet'].keys())
    print(item['snippet']['publishedAt'])
    {
        'title': item['snippet']['title'],
        'description': item['snippet']['description'],
        'channel_id': item['snippet']['channelId'],
        'published_at': item['snippet']['publishedAt']
    }
    title = item['snippet']['title']
    description = item['snippet']['description']
    channel_id = item['snippet']['channelId']
    published_at = item['snippet']['publishedAt']
    video_id = item['snippet']['resourceId']['videoId']
    break
# while snippet_response["nextPageToken"]:

# print(snippet_response.keys())
# print(id_response["items"])
# print(snippet_response["items"][0]["snippet"].keys())
