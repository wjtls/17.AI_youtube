import json
from gtts import gTTS
import os

import os
from bark import generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

def load_content(file_name,country_code): #대사호출
    # 장면추출
    content_list = []
    with open(f'content_data/{country_code}_{file_name}.json', 'r', encoding='utf-8') as file:
        content_json = json.load(file)
    content_data = str(content_json.get('대본'))
    for line in content_data.split("\n"):
        if line.startswith("나래이션"):
            content_list.append(line.replace("나래이션", "").replace(":", "").strip())
    return content_list


def google_tts(content, file_name,country_code):
    print('오디오 저장 대사:', content)

    # Google TTS를 사용하여 음성 생성
    tts = gTTS(text=content, lang=country_code, slow=False) #'zh-cn 중국어, en영어

    # audio_data 폴더가 없으면 생성
    os.makedirs("audio_data", exist_ok=True)

    # 오디오 파일로 저장
    file_path = f"audio_data/{country_code}_{file_name}.wav"
    tts.save(file_path)

    # 저장된 오디오 파일 재생 (Windows)
    # os.system(f"start {file_path}")
    print("대사 오디오 생성완료 :", file_path)


def AI_bark_tts(content, file_name,country_code): #영어만잘함
    print('오디오 저장 대사:', content)
    # 모델 다운로드 및 로드 (처음 실행시에만 다운로드)
    preload_models()

    # 음성 생성
    audio_array = generate_audio(content,  history_prompt=f"v2/{country_code}_speaker_0") #0,1그나마나음

    # audio_data 폴더가 없으면 생성
    os.makedirs("audio_data", exist_ok=True)

    # 오디오 파일로 저장
    file_path = f"audio_data/{country_code}_{file_name}.wav"
    write_wav(file_path, rate=24000, data=audio_array)

    # 저장된 오디오 파일 재생 (Windows)
    #os.system(f"start {file_path}")
    print("대사 오디오 생성완료 :", file_path)


def start(file_name,country_code):
    content_list = load_content(file_name,country_code)
    for idx, content in enumerate(content_list):
        google_tts(content, file_name + f'_{idx}',country_code)
    print('오디오 저장 완료')

if __name__ == '__main__':
    file_name = '테스트_저장_2025-03-27'
    country_code='ja'
    content_list = load_content(file_name,country_code)
    for idx,content in enumerate(content_list):
        google_tts(content,file_name+f'_{idx}',country_code)
        #AI_bark_tts(content,file_name+f'_{idx}')