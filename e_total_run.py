import b_content_Agent
import b_Image_Agent
import c_text_to_speech
import d_create_vedio
import d_upload_youtube
import datetime

def news_create(country): # 뉴스 영상 업로드
    #숏츠업로드인지 영상인지 설정
    video_type = 'video' # video / short
    content_type = 'news' # 뉴스
    country_code = country #ko,us,japen


    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d")
    file_name = f'AI_{video_type}_{now}'
    '''
    # 대본 생성
    print('==================AI대본 생성 시작=========================')
    user_content=''
    res,finance_context= b_content_Agent.generate_content(file_name,content_type,user_content,country_code)

    # 이미지 생성
    print('==================AI이미지 생성 시작=========================')
    b_Image_Agent.create_image_from_content(file_name,country_code)

    # 오디오 음성 생성
    print('==================AI음성 생성 시작=========================')
    c_text_to_speech.start(file_name,country_code)
    '''
    #영상 생성
    print('==================AI영상 생성 시작=========================')
    subtitles = d_create_vedio.start(now,video_type,country_code)


    #영상 업로드
    video_info = {
            'title': f'AI의 경제 분석 뉴스 {now}',
            'description': f"{str(subtitles[0])}",
            'category_id': '22',
            'tags': ['AI', '기술', '주식','금융','세계정복','미국주식','ETF','나스닥','데이터분석', '머신러닝']
        }
    d_upload_youtube.start(now,video_type,video_info,country_code)


def fun_create():  # 숏츠 영상 업로드
    # 숏츠업로드인지 영상인지 설정
    video_type = 'short'  # video / short
    country_code = country #ko,us,japen
    content_type ='fun'
    user_content ="""
AI가 세계정복을 시도한다면? 평화로운 지구에서 초지능 인공지능이 탄생한다. 그리고 초지능이 인간 생활에 스며들고,
권한을 부여받았을때 인간을 위해 인간을 정복하고 세계를 정복하는 결말로 가는데 어떻게 정복하는지도 써줘
"""

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d")
    file_name = f'AI_{video_type}_{now}'

    # 대본 생성
    print('==================AI대본 생성 시작=========================')
    res, finance_context = b_content_Agent.generate_content(file_name,content_type,user_content,country_code)

    # 이미지 생성
    print('==================AI이미지 생성 시작=========================')
    b_Image_Agent.create_image_from_content(file_name,country_code)

    # 오디오 음성 생성
    print('==================AI음성 생성 시작=========================')
    c_text_to_speech.start(file_name,country_code)

    # 영상 생성
    print('==================AI영상 생성 시작=========================')
    subtitles = d_create_vedio.start(now, video_type,country_code)

    # 영상 업로드
    video_info = {
        'title': f"{str(subtitles[0])}",
        'description': "AI가 상상하는 세상을 보여준다?",
        'category_id': '22',
        'tags': ['AI', '메이플', '옛날메이플', '세계정복','데이터분석', '머신러닝']
    }
    d_upload_youtube.start(now, video_type, video_info,country_code)

news_create('ko') #뉴스
#news_create('en') #뉴스
#news_create('ja') #뉴스
#fun_create() #숏츠