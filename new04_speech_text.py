import os
from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()  # openai_key .env 선언 사용
import dongsooAI as ds
from openai import OpenAI

client = OpenAI()

audio_file= open("talkAI/text_speech.mp3", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file,
  response_format="text"
)
print( transcript )