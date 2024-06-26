# -*- coding: utf-8 -*-
"""YT-analysis-project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p4hOpHCD3Zl38yNPGY_X_44QnFir1gck
"""

from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = 'AIzaSyD5kgNaKgOsDWODIJSpfgQPfuEov7gqh1A'
channel_ids = ['UCBwmMxybNva6P_5VmxjzwqA', #apna college
             'UCeVMnSShP_Iviwkknt83cww', #codewithharry
             'UCzYHY5ngRe4hYclT-tLCJoQ', #manthan
             'UCTlnaHHQ75zlDg_fLr7tGEg', #timeliners
             'UCdxbhKxr8pyWTx1ExCSmJRw' #girliyapa
             ]


youtube = build('youtube','v3',developerKey=api_key)

## function to get channel statistics
def get_channel_stats(youtube, channel_ids):
  all_data = []
  request = youtube.channels().list(
      part = 'snippet,contentDetails,statistics',  ##parameters
      id = ','.join(channel_ids))
  response = request.execute()

  for i in range (len(response['items'])):
    data = dict(channel_name = response['items'][i]['snippet']['title'],
              subscribers = response['items'][i]['statistics']['subscriberCount'],
              Views = response['items'][i]['statistics']['viewCount'],
              total_videos = response['items'][i]['statistics']['videoCount'],
              playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
    all_data.append(data)

  return all_data

channel_stats = get_channel_stats(youtube, channel_ids)

channel_data = pd.DataFrame(channel_stats)
channel_data

channel_data['subscribers'] = pd.to_numeric(channel_data['subscribers'].astype(int))
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['total_videos'] = pd.to_numeric(channel_data['total_videos'])

channel_data.dtypes

print(channel_data['subscribers'].min())
print(channel_data['subscribers'].max())

sns.set(rc={'figure.figsize':(8,6)})
ax = sns.barplot(x='channel_name', y='subscribers',data=channel_data)

ax.set_xlabel('Channel Name', fontsize=12)  # X-axis label
ax.set_ylabel('subscribers', fontsize=12)   # Y-axis label

# Rotate x-axis labels for better readability (if needed)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

ax = sns.barplot(x='channel_name', y='Views',data=channel_data)

ax = sns.barplot(x='channel_name', y='total_videos',data=channel_data)

channel_data

playlist_id = channel_data.loc[channel_data['channel_name']=='Apna College','playlist_id'].iloc[0]



# Function to get video ids
def get_video_ids(youtube, playlist_id):
  request = youtube.playlistItems().list(
      part = 'contentDetails',
      playlistId = playlist_id,
      maxResults = 50)
  response = request.execute()

  video_ids = []

  for i in range(len(response['items'])):
    video_ids.append(response['items'][i]['contentDetails']['videoId'])

  next_page_token = response.get('nextPageToken')
  more_pages = True

  while more_pages:
    if next_page_token is None:
      more_pages = False
    else:
      request = youtube.playlistItems().list(
          part = 'contentDetails',
          playlistId = playlist_id,
          maxResults = 50,
          pageToken = next_page_token)
      response = request.execute()

      for i in range (len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

      next_page_token = response.get('nextPageToken')

  #return len(video_ids)
  return video_ids

video_ids = get_video_ids(youtube, playlist_id)

len(video_ids)

video_ids

#function to get video details

def get_video_details(youtube, video_ids):
    all_video_stats = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i+50]))  # we can only pass 50 ids at a time
        response = request.execute()

        if 'items' in response:
            for video in response['items']:
                video_stats = {
                    'Title': video['snippet']['title'],
                    'Published_date': video['snippet']['publishedAt'],
                    'Views': video['statistics']['viewCount'],
                    'Likes': video['statistics']['likeCount'],
                    'Comments': video['statistics']['commentCount']
                }
                all_video_stats.append(video_stats)
        else:

            print(f"Error: Response is missing 'items' for IDs {video_ids[i:i+50]}")

    return all_video_stats

get_video_details(youtube, video_ids)

video_details = get_video_details(youtube, video_ids)

video_data = pd.DataFrame(video_details)

video_data

video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])

video_data['Comment'] = pd.to_numeric(video_data['Comments'])
video_data

top10_videos = video_data.sort_values(by ='Views', ascending = False).head(10)
top10_videos

sns.set(rc={'figure.figsize':(10,8)})
ax1 = sns.barplot(x = 'Views', y = 'Title', data = top10_videos)

video_data

video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')

video_data

videos_per_month = video_data.groupby('Month', as_index = False).size()
videos_per_month

sort_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
videos_per_month.sort_index()

videos_per_month = videos_per_month.sort_index()

ax2 = sns.barplot(x='Month', y='size', data= videos_per_month)





