import json
import os.path
from helpers.youtube import get_playlist_info, get_playlist_name

url_link = 'https://www.youtube.com/playlist?list=PL4AWxkId50utoYIbd64M7E1IzTu6ZYadt'
playlist_id = url_link.split('=')[1]

# Get playlist name and dictionary of videos in playlist
playlist_name = get_playlist_name(playlist_id)
videos = get_playlist_info(playlist_id)

# Generate filepaths
filepath = f'./playlists/{playlist_name}.json'
log_filepath = f'./playlists/{playlist_name}_log.txt'

# If file does not exist, make a new one to make sure script don't crash
if not os.path.exists(filepath):
    with open(filepath, 'w') as f:
        pass

with open(filepath, 'r', encoding='utf-8') as fin:
    with open(log_filepath, 'w', encoding='utf-8') as fout:
        data = fin.read()
        data = {} if len(data) <= 1 else json.loads(data)

        newdata = {}

        # Check for any videos deleted
        for key in data:
            if key not in videos:
                string = f'- Title: {data[key]["title"]}\n\tChannelId: {data[key]["channel_id"]}\n\tVideoId: {data[key]["video_id"]}\n'
                fout.write(string)
            newdata[key] = data[key]

        # Check for any videos added
        for key in videos:
            if key not in data:
                string = f'+ Title: {videos[key]["title"]}\n\tChannelId: {videos[key]["channel_id"]}\n\tVideoId: {videos[key]["video_id"]}\n'
                fout.write(string)
            newdata[key] = videos[key]

if newdata:
    with open(filepath, 'w') as fout:
        pass
    with open(filepath, 'w', encoding='utf-8') as fout:
        data = json.dumps(newdata, indent=4, ensure_ascii=False)
        fout.write(data)
