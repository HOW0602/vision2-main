from flask import Flask, request, jsonify
import os
import requests
import random
import string
import base64
from openai import OpenAI
from pathlib import Path
import pygame
import chatDbFun as chatDB
from dotenv import load_dotenv

# OpenAI API 키를 .env 파일에서 로드
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# API 키가 없으면 에러 발생
if not api_key:
    raise ValueError("No API key provided. Set the OPENAI_API_KEY environment variable.")

def folder(directory_name):
    # 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    # 디렉토리 경로 반환
    return directory_name

def rnd_str(n=5, type="ns"):
    # 랜덤 문자열 생성
    if type == "n":
        characters = string.digits
    elif type == "s":
        characters = string.ascii_letters
    else:  # "ns" 또는 다른 경우
        characters = string.digits + string.ascii_letters
    return ''.join(random.choices(characters, k=n))

@app.route('/save_image', methods=['POST'])
def save_image():
    # 전송된 이미지 경로 가져오기
    generated_image_path = request.form.get('generated_image_path')

    if generated_image_path:
        # 이미지 저장 및 저장된 이미지 경로 반환
        saved_image_path = image_create(generated_image_path, folder_name="saved_images")

        # 저장된 이미지 경로를 JSON 형식으로 응답
        return jsonify({'saved_image_path': saved_image_path})
    else:
        return jsonify({'error': 'Generated image path not provided'})

def image_create(prompt="ex:탕후루를 먹었다 이빨이 아파서 병원에 갔다 치료를 하고 잠에 들었다", size="1024x1024", quality="standard", n=1):
    # OpenAI 클라이언트 생성
    client = OpenAI()

    # 이미지 생성 요청
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt + "A four-cut cute Korean cartoon. There's no writing no word no text!!  ",
        size=size,
        quality=quality,
        n=n,
    )

    # 이미지 데이터
    image_data = {
        "revised_prompt": response.data[0].revised_prompt,
        "url": response.data[0].url
    }

    return image_data
