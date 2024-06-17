

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import pandas as pd
import googleapiclient.discovery


def process_comments(response_items):
    comments = []
    for comment in response_items:
        id = comment['id']
        author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
        like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']
        publish_time = comment['snippet']['topLevelComment']['snippet']['publishedAt']
        #replies = comment['replies']['comments']['snippet']
        comment_info = {'id': id, 'author': author, 'comment':comment_text, 'published_at': publish_time, 'like': like_count}
        comments.append(comment_info)
        print(f'Fininshed Processing {len(comments)} comments.')
        return comments

def run_youtube_etl():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBu00mAZpcmSBCCElo0zQW8EEPET3lHaqA"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id,snippet,replies",
        maxResults=1,
        videoId="q8q3OFFfY6c"
    )
    response = request.execute()

    # print(response)
    comments = process_comments(response['items'])
    df = pd.DataFrame(comments)
    print(df)

    df.to_csv('youtube_video_data.csv')
