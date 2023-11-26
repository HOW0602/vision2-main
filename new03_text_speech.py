import os
from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()  # openai_key .env 선언 사용
import dongsooAI as ds
import pygame
from openai import OpenAI
import base64

client = OpenAI()

#  voices -> alloy, echo, fable, onyx, nova, shimmer 

response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input="""
    저는 제돌입니다.
    """    
    )

#encoded_audio = base64.b64encode(response.content).decode('utf-8')     
print(response.content )

response.stream_to_file("talkAI/jedol.mp3")
 
pygame.mixer.init()
pygame.mixer.music.load("talkAI/jedol.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy(): 
    pygame.time.Clock().tick(10)

pygame.mixer.music.stop()
pygame.mixer.quit()

