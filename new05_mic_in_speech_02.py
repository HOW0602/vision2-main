# 필요한 라이브러리를 불러옵니다.
import os
import speech_recognition as sr
import pygame
from openai import OpenAI
from io import BytesIO
from dotenv import load_dotenv

# .env 파일에서 환경변수를 로드합니다.
load_dotenv()

# OpenAI 클라이언트를 초기화합니다.
client = OpenAI()

# SpeechRecognition 설정
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Pygame mixer 초기화
pygame.mixer.init()

try:
    while True:
        # 마이크로부터 입력을 받습니다.
        with mic as source:
            print("말씀하세요: ")
            audio_data = recognizer.listen(source)
            try:
                # Google 음성 인식을 사용하여 텍스트로 변환합니다.
                query = recognizer.recognize_google(audio_data, language="ko-KR")
            except sr.UnknownValueError:
                print("인식할 수 없는 오디오입니다.")
                continue
            except sr.RequestError as e:
                print(f"음성 인식 서비스 요청 실패: {e}")
                continue
            
            # "종료"가 인식되면 루프를 종료합니다.
            if "종료" in query:
                print("종료합니다.")
                break
            
            print(f"you = {query}")
            
            # GPT-4를 사용하여 답변을 생성합니다.
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {"role": "system", "content": '매우 간결하게 답변합니다.' },
                    {"role": "user", "content": f'{query}' }],
                max_tokens=1000,
            )
            ans = response.choices[0].message.content
            
            
            # 생성된 답변을 음성으로 변환합니다.
            audio_response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=ans
            )
            # print(f"ans = {ans}\n")
            # 변환된 음성을 재생합니다.
            # print(audio_response.content)
            audio_file = BytesIO(audio_response.content)  # 음성 데이터를 BytesIO 객체로 변환
            pygame.mixer.music.load(audio_file, 'mp3')
            pygame.mixer.music.play()
            
            # 음성 재생이 끝날 때까지 대기합니다.
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
finally:
    # Pygame 종료 처리
    pygame.mixer.quit()
    # 마이크 종료 처리
    if 'mic' in locals():
        mic.__exit__()
