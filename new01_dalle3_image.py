from openai import OpenAI
import  dongsooAI as ds
from dotenv import load_dotenv;load_dotenv()  # openai_key .env 선언 사용
client = OpenAI()

print("Start--귀여운 고양이 이미지 만들기------------------------------")

response = client.images.generate(
  model="dall-e-3",
  prompt="귀여운 고양이",
  size="1024x1024",
  quality="standard",
  n=1,
)

print( response.data[0] )
print( "ok------------------------")

print()
print("귀여운고양이.png -------------saved!")
image_url = response.data[0].url
image_namne=ds.image_url_to_save( image_url,"images","귀여운고양이.png")
print( "ok------------------------")
print(f"Saved! {image_namne}")
