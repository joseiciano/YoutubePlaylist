import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json
import sqlite3

load_dotenv()
API_KEY = os.getenv("API_KEY")

youtube = build('youtube', 'v3', developerKey=API_KEY)

url_link = 'https://www.youtube.com/playlist?list=PL4AWxkId50utoYIbd64M7E1IzTu6ZYadt'
playlist_id = url_link.split('=')[1]


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


# Get playlist name and dictionary of videos in playlist
playlist_name = get_playlist_name(playlist_id)
videos = get_playlist_info(playlist_id)

# Open database (if exists)
conn = sqlite3.connect('playlists.db')
c = conn.cursor()

# Sanity check tables
c.execute('''CREATE TABLE IF NOT EXISTS
            ? (title text, channel_id text, published_at text, video_id text)''', (playlist_name,))
c.execute('''CREATE TABLE IF NOT EXISTS deleted (title text, channel_id text, published_at text, video_id text)''')

# Load all videos in playlist and check if it is in the videos dict.
c.execute("SELECT * FROM playlist")
db_vids = c.fetchall()

# Check if each video in db is in our videos dict. If not, it got removed
with open('log.txt', 'w') as f:
    pass
with open('log.txt', 'a') as f:
    for video in db_vids:
        if video['video_id'] not in videos:
            f.write(f"- NAME: {video['title']}, ID: {video['video_id']}")
            c.execute("INSERT INTO ? VALUES (?, ?, ?, ?)", (
                playlist_name, video['title'], video['channel_id'], video['published_at'], video['video_id']))
            c.execute("DELETE FROM ? WHERE video_id=?",
                      (playlist_name, video['video_id'],))

    # Now check if each video in videos are in db. If not, we added a video
    for video in videos.values():
        c.execute("SELECT * FROM playlist where video_id=?",
                  (video['video_id'],))
        db_vids = c.fetchall()

        if not db_vids:
            f.write(f"+ NAME: {video['title']}, ID: {video['video_id']}")
            c.execute("INSERT INTO ? VALUES (?, ?, ?, ?)", (playlist_name,
                                                            video['title'], video['channel_id'], video['published_at'], video['video_id']))

conn.commit()
conn.close()
