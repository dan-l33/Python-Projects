# Input channel home URL to get dataset of uploaded videos
# Tutorials followed below
# https://www.youtube.com/watch?v=KcPimbou-kI
# https://www.youtube.com/watch?v=D56_Cx36oGY

import os
import config
#import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import json
from dateutil import parser


#channel_ids = []

url  = input("Enter url of channel home e.g. https://www.youtube.com/@Formula1: ")
soup = BeautifulSoup(requests.get(url, cookies={"CONSENT": "YES+1"}).text, "html.parser")

data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)

json_data = json.loads(data)

channel_id = json_data["header"]["c4TabbedHeaderRenderer"]["channelId"]

#channel_ids.append(channel_id)

youtube = build("youtube", "v3", developerKey = config.YouTube_API)

#channel_ids = ["UC073quTeFarhKNe8ZuC6Qig",]

def get_channel_stats(youtube, channel_ids):
    all_data = []

    request = youtube.channels().list(
        part = "snippet,contentDetails,statistics",
        #id = ",".join(channel_ids))
        id = channel_id)

    response = request.execute()

    #print(response)

    for item in response ["items"]:
        global playlist_id
        data = {"channelName": item["snippet"]["title"],
                "subscribers": item["statistics"]["subscriberCount"],
                "views": item["statistics"]["viewCount"],
                "totalVideos": item["statistics"]["videoCount"],
                "playlistId": item["contentDetails"]["relatedPlaylists"]["uploads"]}

        playlist_id = item["contentDetails"]["relatedPlaylists"]["uploads"]

        all_data.append(data)

    return(pd.DataFrame(all_data))

channel_stats = get_channel_stats(youtube, channel_id)
print(channel_stats)

#playlist_id = "UU073quTeFarhKNe8ZuC6Qig"

def get_video_ids(youtube, playlist_id):
    video_ids = []

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50)
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token)
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')

    return video_ids

video_ids = get_video_ids(youtube, playlist_id)
#print(video_ids)


def get_video_details(youtube, video_ids):
    all_video_info = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i + 50])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                             }
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)

    return pd.DataFrame(all_video_info)

video_df = get_video_details(youtube, video_ids)
#print(video_df)

# Convert count columns to numeric
numeric_cols = ['viewCount', 'likeCount', 'favouriteCount', 'commentCount']
video_df[numeric_cols] = video_df[numeric_cols].apply(pd.to_numeric, errors = 'coerce', axis = 1)

# Publish day in the week
video_df['publishedAt'] = video_df['publishedAt'].apply(lambda x: parser.parse(x))
video_df['pushblishDayName'] = video_df['publishedAt'].apply(lambda x: x.strftime("%A"))

import isodate
video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x))
video_df['durationSecs'] = video_df['durationSecs'].astype('timedelta64[s]')

video_df[['durationSecs', 'duration']]

video_df.to_csv('YouTubeData.csv', index=False, encoding='utf-8')