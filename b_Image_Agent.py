# 이미지 생성

import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types



from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# API 키 정보 로드
load_dotenv(override=True)

def Agent_gemini(contents,image_name):

    # Google Generative AI 클라이언트 초기화
    client = genai.Client()

    # 이미지 생성 요청
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']  # 텍스트와 이미지 출력 요청
        )
    )

    # 응답 처리: 이미지 저장 및 출력
    for candidate in response.candidates:
        for part in candidate.content.parts:
            if part.text is not None:
                print("Generated Text:", part.text)  # 생성된 텍스트 출력
            elif part.inline_data is not None:
                # 이미지 데이터를 처리하여 저장
                image = Image.open(BytesIO(part.inline_data.data))
                image.save(f'Image_data/{image_name}.png')
                #image.show()  # 생성된 이미지를 화면에 표시
    print(f'AI 이미지 {image_name} 생성완료')


def Agent_Imagen(contents, image_name):
    client = genai.Client()
    max_retries = 2
    retry_delay = 10

    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=contents,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1"
                )
            )

            if response and response.generated_images:
                for generated_image in response.generated_images:
                    image = Image.open(BytesIO(generated_image.image.image_bytes))
                    image.save(f'Image_data/{image_name}.png')
                    #image.show()
                print(f'AI 이미지 {image_name} 생성 완료')
                time.sleep(2)
                return  # 성공적으로 이미지를 생성했으므로 함수 종료

            elif attempt < max_retries:
                print(f"응답이 비어있습니다. {retry_delay}초 후 재시도합니다. (시도 {attempt + 1}/{max_retries + 1})")
                time.sleep(retry_delay)
            else:
                print(f"최대 재시도 횟수({max_retries})를 초과했습니다. 이미지 생성에 실패했습니다.")

        except Exception as e:
            if attempt < max_retries:
                print(f"오류 발생: {str(e)}. {retry_delay}초 후 재시도합니다. (시도 {attempt + 1}/{max_retries + 1})")
                time.sleep(retry_delay)
            else:
                print(f"최대 재시도 횟수({max_retries})를 초과했습니다. Dalle로 생성시작,,,, 오류: {str(e)}")
                Agent_DALLE3(contents, image_name)



import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image
import os

def Agent_stable(contents, image_name):
    # SDXL 파이프라인 초기화
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    )
    pipe.to("cuda")

    # 이미지 생성
    image = pipe(prompt=contents).images[0]

    # 이미지 저장
    os.makedirs("Image_data", exist_ok=True)
    image.save(f"Image_data/{image_name}.png")
    image.show()  # 생성된 이미지를 화면에 표시

    print(f'AI 이미지 {image_name} 생성 완료')



def Agent_DALLE3(contents, image_name):
    # OpenAI 클라이언트 초기화
    client = OpenAI()

    # DALL-E 3를 사용한 이미지 생성 요청
    response = client.images.generate(
        model="dall-e-3",
        prompt=contents,
        size="1024x1024",
        quality="hd", #standard,hd
        n=1,
    )

    # 응답 처리: 이미지 저장
    image_url = response.data[0].url
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        image = Image.open(BytesIO(image_response.content))
        image.save(f'Image_data/{image_name}.png')
        print(f'AI 이미지 {image_name} 생성 완료')
    else:
        print("이미지 생성에 실패했습니다.")

def create_image_from_content(save_file_name,country_code): #대본으로 이미지생성
    # 장면추출
    scene_list = []
    with open(f'content_data/{country_code}_{save_file_name}.json', 'r', encoding='utf-8') as file:
        content_json = json.load(file)
    content_data = str(content_json.get('대본'))
    for line in content_data.split("\n"):
        if line.startswith("장면"):
            scene_list.append(line.replace("장면 :", "").strip())

    for step, scene_data in enumerate(scene_list):
        print("생성 이미지 장면 내용 : ",scene_data)
        scene_data = "Photorealistic render of a"+str(scene_data)+',ultra-high quality image,Realistic background'
        Agent_Imagen(scene_data, str(save_file_name) + f'_{step}')  # 이미지생성후 저장 가장 실사와 유사
        #Agent_gemini(scene_data, str(save_file_name)+f'_{step}')  # 이미지생성후 저장
        #Agent_stable(scene_data, str(save_file_name)+f'_{step}')
        #Agent_DALLE3(scene_data, str(save_file_name)+f'_{step}')
        time.sleep(10)


if __name__ == '__main__':
    # 생성된 대본에서 이미지 생성
    country_code= 'ja'
    create_image_from_content("테스트_저장_2025-03-27",country_code)