
import speech_recognition as sr
import pygame

# SpeechRecognition 설정
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Pygame mixer 초기화
pygame.mixer.init()

try:
    while True:
        # 마이크로부터 입력을 받습니다.
        with mic as source:
            print("Listening: ")
            audio_data = recognizer.listen(source)
            try:
                # Google 음성 인식을 사용하여 텍스트로 변환합니다.
                text = recognizer.recognize_google(audio_data, language="ko-KR")
            except sr.UnknownValueError:
                print("인식할 수 없는 오디오입니다.")
                continue
            except sr.RequestError as e:
                print(f"음성 인식 서비스 요청 실패: {e}")
                continue
            
            # "종료"가 인식되면 루프를 종료합니다.
            if "종료" in text:
                print("종료합니다.")
                break
            
            print(f"text = {text}")
            
          
            
finally:
    # Pygame 종료 처리
    pygame.mixer.quit()
    # 마이크 종료 처리
    if 'mic' in locals():
        mic.__exit__()
