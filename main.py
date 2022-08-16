# main file
import pandas as pd

def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part='snippet, contentDetails, statistics',
        id=','.join(channel_ids))
    
    response = request.execute()
    
    for i in range(len(response['items'])):
        data = dict(
                    channel_name = response['items'][i]['snippet']['title'],
                    subscribers = response['items'][i]['statistics']['subscriberCount'],
                    total_views = response['items'][i]['statistics']['viewCount'],
                    video_count = response['items'][i]['statistics']['videoCount'],
                    playlistId = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                    )
        all_data.append(data)
        
    return pd.DataFrame(all_data)
    

def get_response_json(youtube, channel_ids):
    request = youtube.channels().list(
        part='snippet, contentDetails, statistics',
        id=','.join(channel_ids))

    response = request.execute()
    
    return JSON(response)


def get_channel_stats_json(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part='snippet, contentDetails, statistics',
        id=','.join(channel_ids))
    
    response = request.execute()
    
    for i in range(len(response['items'])):
        data = dict(
                    channel_name = response['items'][i]['snippet']['title'],
                    subscribers = response['items'][i]['statistics']['subscriberCount'],
                    total_views = response['items'][i]['statistics']['viewCount'],
                    video_count = response['items'][i]['statistics']['videoCount'],
                    playlistId = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                    )
        all_data.append(data)
        
    return all_data

# channel_statistics_json = get_channel_stats_json(youtube, channel_ids)
# channel_statistics_json
# get playlist

def get_playlist(youtube, channel_statistics):
    playlist_ids = []
    for playlist_id in channel_statistics['playlistId']: 
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId = playlist_id
        )
        response = request.execute()
        playlist_ids.append(playlist_id)

    return playlist_ids
        # revise: need to return pairs of channel_name, playlist_id
        

def get_video_ids(youtube, playlist_id):
        video_ids = []

        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId = playlist_id,
            maxResults = 50 # get max result, not just 5 video ids
        )
        response = request.execute()

        for video_id in response['items']: 
            video_ids.append(video_id['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        while next_page_token is not None:
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId = playlist_id,
                maxResults = 50,
                pageToken = next_page_token
            )

            response = request.execute()

            for video_id in response['items']: 
                video_ids.append(video_id['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

        return video_ids
        # revise: return all video_ids for given channel

def get_video_details(youtube, video_ids):
    all_video_info = []
    video_info = {}

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=','.join(video_ids)
    )
    response = request.execute()

    # for video in response['items']:
    video = response['items']
    for i in range(len(response['items'])):
        video_data = dict(
            video_id = video[i]['id'],
            title = video[i]['snippet']['title'],
            description = video[i]['snippet']['description'],
            tags = video[i]['snippet']['tags'],
            published_at = video[i]['snippet']['publishedAt'],
            thumbnails = video[i]['snippet']['thumbnails']['high']['url'],
            view_count = video[i]['statistics']['viewCount'],
            like_count = video[i]['statistics']['likeCount'],
            comment_count = video[i]['statistics']['commentCount'],
            duration = video[i]['contentDetails']['duration'],
            definition = video[i]['contentDetails']['definition'],
            caption = video[i]['contentDetails']['caption'],
        )
        all_video_info.append(video_data)
    return pd.DataFrame(all_video_info)


def get_comments_in_videos(youtube, video_ids):
    all_comments = []
    for video_id in video_ids:
        try:   
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id
            )
            response = request.execute()
        
            comments_in_video = [comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in response['items'][:]]
            comments_in_video_info = {'video_id': video_id, 'comments': comments_in_video}

            all_comments.append(comments_in_video_info)
            
        except: 
            # When error occurs - most likely because comments are disabled on a video
            print('Could not get comments for video ' + video_id)
        
    return pd.DataFrame(all_comments) 
