import os
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# OAuth 2.0 인증
SCOPES = [os.environ["SCOPES1"], os.environ["SCOPES2"]]


def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file('GCP_youtube_secret_key.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=credentials)


def upload_video(youtube, file, title, description, category_id, tags):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': 'public'  # 'private', 'unlisted'도 가능
        }
    }

    media = MediaFileUpload(file, chunksize=-1, resumable=True, mimetype='video/*')
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f'Uploading... {int(status.progress() * 100)}%')

    print(f'Video uploaded: {response["id"]}')
    return response['id']


def set_thumbnail(youtube, video_id, thumbnail_file):
    request = youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumbnail_file))
    response = request.execute()
    print(f'Thumbnail set: {response}')

def start(date,video_type,video_info,country_code):
    youtube = authenticate_youtube()
    file_path = f'AI_video_{country_code}_{date}_{video_type}.mp4'
    title = video_info.get('title')  # 기본값 설정
    description = video_info.get('description')  # 기본값 설정
    category_id = video_info.get('category_id')  # 기본값 설정
    tag = video_info.get('tags')  # 기본값 설정
    # 동영상 업로드
    video_id = upload_video(youtube, file_path, title, description, category_id, tag)

    # 썸네일 설정 (동영상의 첫 번째 프레임을 이미지로 저장한 후 사용해야 함)
    # 예를 들어, 'thumbnail.jpg'라는 파일로 저장했다고 가정

    set_thumbnail(youtube, video_id, f'썸네일_{date}_{video_type}.jpg')
    print('유튜브 업로드 완료')

if __name__ == '__main__':
    date= "2025-03-27"
    video_type ="short" # short ,video
    country_code= 'ja'
    video_info = {
        'title': '내가 만든 AI 비디오',
        'description': '이 비디오는 AI에 대한 분석을 제공합니다.',
        'category_id': '22',
        'tags': ['AI', '기술', '주식','금융','세계정복','미국주식','ETF','나스닥','데이터분석', '머신러닝']
    }
    start(date,video_type,video_info,country_code)