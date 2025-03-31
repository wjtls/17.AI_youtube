import os
import json
from moviepy.editor import *
from moviepy.video.fx.all import resize
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import re


def start(date_str,video_type,country_code):
    # 경로 설정
    image_path = r"D:\AI_pycharm\pythonProject\3_AI_LLM_finance\b_youtube_AI\Image_data"
    content_path = r"D:\AI_pycharm\pythonProject\3_AI_LLM_finance\b_youtube_AI\content_data"
    audio_path = r"D:\AI_pycharm\pythonProject\3_AI_LLM_finance\b_youtube_AI\audio_data"

    def sort_by_last_number(file_list): #파일내 마지막 숫자로 정렬
        def extract_number(filename):
            match = re.search(r'_(\d+)\.[a-zA-Z]+$', filename)
            return int(match.group(1)) if match else 0

        return sorted(file_list, key=extract_number)

    # 파일 찾기
    image_files = sorted([f for f in os.listdir(image_path) if f.endswith('.png') and f"{video_type}_{date_str}" in f])
    json_files = sorted([f for f in os.listdir(content_path) if f.endswith('.json') and f"{country_code}_AI_{video_type}_{date_str}" in f])
    audio_files = sorted([f for f in os.listdir(audio_path) if f.endswith('.wav') and f"{country_code}_AI_{video_type}_{date_str}" in f])

    # 마지막 숫자로 정렬
    image_files = sort_by_last_number(image_files)
    json_files = sort_by_last_number(json_files)
    audio_files = sort_by_last_number(audio_files)

    print(image_files)
    print(json_files)
    print(audio_files)
    def load_content(file_name, types):
        content_list = []
        with open(os.path.join(content_path, file_name), 'r', encoding='utf-8') as file:
            content_json = json.load(file)
        content_data = str(content_json.get('대본'))
        for line in content_data.split("\n"):
            if line.startswith(types):
                content_list.append(line.replace(types, "").replace(":", "").strip())
        return content_list

    def add_text_to_image(image, text):
        pil_image = Image.fromarray(np.uint8(image)).convert("RGB")
        draw = ImageDraw.Draw(pil_image)
        font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # 한글 폰트 경로
        font = ImageFont.truetype(font_path, 36)
        text_width, text_height = draw.textsize(text, font=font)

        text_height = text_height + 170
        position = ((pil_image.width - text_width) // 2, pil_image.height - text_height - 20)

        # 텍스트를 여러 번 그려서 두께를 증가시킴
        for offset in range(-2, 3):  # -2, -1, 0, 1, 2의 오프셋으로 겹쳐서 그림
            draw.text((position[0] + offset, position[1]), text, font=font, fill=(255, 255, 255))

        return np.array(pil_image)

    # JSON 파일에서 자막 텍스트 가져오기
    subtitles = []
    for json_file in json_files:
        subtitles.extend(load_content(json_file, '타이틀'))

    # 이미지 클립 생성 (자막 포함)
    image_clips = []
    for img_file, subtitle in zip(image_files, subtitles):
        img = ImageClip(os.path.join(image_path, img_file))
        if video_type =='video':
            img = img.resize(newsize=(1280, 720))  # 가로 1280, 세로 720으로 설정(숏츠말고 영상업로드)

            print('유튜브 영상용 생성')
        if video_type == 'short':
            print('유튜브 숏츠용 생성')

        img = img.fl_image(lambda x: add_text_to_image(x, subtitle))  # 자막 추가
        image_clips.append(img)

    # 오디오 클립 생성
    audio_clips = [AudioFileClip(os.path.join(audio_path, audio_file)) for audio_file in audio_files]

    # 각 오디오와 이미지를 매치시켜 개별 비디오 클립 생성
    video_clips = []
    for audio_clip, image_clip in zip(audio_clips, image_clips):
        # 이미지 클립의 지속 시간을 오디오 클립과 동일하게 설정
        image_clip = image_clip.set_duration(audio_clip.duration)

        # 오디오를 이미지에 추가하여 비디오 클립 생성
        video_clip = image_clip.set_audio(audio_clip)
        video_clips.append(video_clip)

    # 모든 비디오 클립을 연결
    final_video = concatenate_videoclips(video_clips)

    # 최종 비디오 생성 및 저장
    final_video.write_videofile(f"AI_video_{country_code}_{date_str}_{video_type}.mp4", fps=30, codec="mpeg4", bitrate="5000k")

    print("비디오 생성 완료")



    #썸네일 저장
    from moviepy.editor import VideoFileClip
    # 비디오 파일 경로
    video_path = f"AI_video_{country_code}_{date_str}_{video_type}.mp4"
    # 비디오 파일 열기
    video = VideoFileClip(video_path)
    # 첫 번째 프레임을 이미지로 저장
    video.save_frame(f"썸네일_{date_str}_{video_type}.jpg", t=0)  # t=0은 비디오의 첫 번째 프레임을 의미
    # 비디오 클립 닫기
    video.close()
    print('썸네일 생성 완료')
    return subtitles


if __name__ == '__main__':
    date="2025-03-27"
    video_type="테스트_저장" #video,short
    country_code='ja'
    start(date,video_type,country_code)