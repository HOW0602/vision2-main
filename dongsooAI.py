from flask import Flask, session, request, render_template, jsonify ,session

import os
import requests
import random
import string
import base64
from openai import OpenAI
from pathlib import Path
import pygame
import chatDbFun as chatDB
from dotenv import load_dotenv;load_dotenv()  # openai_key .env 선언 사용

api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)

if not api_key:
   raise ValueError("No API key provided. Set the OPENAI_API_KEY environment variable.")

def folder(directory_name):
    # Create a directory if it doesn't exist
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    # Return the path to the directory
    return directory_name

def rnd_str(n=5, type="ns"):
    # Generate a random string
    if type == "n":
        characters = string.digits
    elif type == "s":
        characters = string.ascii_letters
    else:  # "ns" or other
        characters = string.digits + string.ascii_letters
    return ''.join(random.choices(characters, k=n))

@app.route('/save_image', methods=['POST'])
def save_image():
    # 가져온 이미지 경로
    generated_image_path = request.form.get('generated_image_path')

    if generated_image_path:
        # 이미지를 저장하고 저장된 이미지의 경로를 반환
        saved_image_path = image_create(generated_image_path, folder_name="saved_images")

        # 저장된 이미지의 경로를 JSON 형식으로 응답
        return jsonify({'saved_image_path': saved_image_path})
    else:
        return jsonify({'error': 'Generated image path not provided'})
    

def image_create(prompt="탕후루를 먹었다 이빨이 아파서 병원에 갔다 치료를 하고 잠에 들었다",size="1024x1024", quality="standard",n=1):
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt+"in four cut korean cartoon with in reality  without any text",
        size=size,
        quality=quality,
        n=n
        )
    
    # print( response.data[0])
    
    image_data = {
        "revised_prompt": response.data[0].revised_prompt,
        "url": response.data[0].url
    }

    return image_data


# def mp3_play(mp3_file, remove=True):
#     try:
#         pygame.mixer.init()
#         pygame.mixer.music.load(mp3_file)
#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy(): 
#             pygame.time.Clock().tick(10)
    
#     finally:  
#         pygame.mixer.music.stop()
#         pygame.mixer.quit()
#         if remove:
#             os.remove(mp3_file)

    
# def chatGPT_tts( query="",voice="nova",chat_id="",chat_story="",token=""):
   
#     client = OpenAI()
    
#     chat_history=chatDB.query_history(token) # 기존 대화 내용

#     prompt=[]
#     prompt.append({"role": "system", "content": f"{chat_story}"  })
#     prompt=prompt + chat_history
#     prompt.append({"role": "system", "content": "자세하게 설명하라는 말이 없으면, 가능한 간결하게 대답한다." })
#     prompt.append({"role": "user", "content": query })
     
#     response  = client.chat.completions.create(
#                                 model="gpt-4-vision-preview",
#                                 messages=prompt,
#                                  max_tokens=1000,
#      ) 
#     answer=response.choices[0].message.content 
#     new_chat=[{"role": "user", "content": query },{"role": "assistant", "content":answer}]

#     Path("templates/chat_audio").mkdir(parents=True, exist_ok=True)
#     speech_file_path = f"templates\\chat_audio\\{chat_id}.mp3"
#     response = client.audio.speech.create(
#             model="tts-1",
#             voice="alloy",
#             input=answer)
#     response.stream_to_file(speech_file_path)
    
#     answer_no_update = any( chat["content"] == answer  for chat in chat_history)
#     checkMsg=["죄송합니다","확인하십시요","OpenAI","불가능합니다","미안합니다.","않았습니다","언제든지","필요하시면 다시 말씀해주세요"]
#     for a in checkMsg: 
#         if a in answer:
#            answer_no_update=True
#            break
    
#     # 새로운 대화 내용을 업데이트
#     if not answer_no_update and not 'test' in token:
#         chatDB.update_history(token, new_chat, max_token=5000)

#     re={
#         "answer":answer
#         #"answer_audio_base64":encoded_audio
#     }
#     return re

# if __name__ == '__main__':
    
#     print()
#     re=image_url_to_save("https://www.jeju.go.kr/files/editor/4f81874a-321d-4926-a34e-c09cadd33fce.jpg","images",image_name="백록담.png")
#     print("image url를 파일로 저장 = ", re)
#     print()


#     re=image_tobase64_image( "images/백록담.png" )
#     print("image/백록담.png------Convert the image file to a base64 text string.----------")
#     print(f"{re[:30]} ... 중략 ... {re[-30:]}")
#     print()

#     re=vision_talk( image_infor="https://www.jeju.go.kr/files/editor/4f81874a-321d-4926-a34e-c09cadd33fce.jpg" )
#     print( re )
#     print( re["content"] )


#     print("dalle3 이미지 생셩")
#     re=image_create()
#     print( re )
