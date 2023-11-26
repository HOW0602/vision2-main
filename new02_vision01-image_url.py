import os
from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()  # openai_key .env 선언 사용

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
   raise ValueError("No API key provided. Set the OPENAI_API_KEY environment variable.")

def vison_talk( image_url ):
    client = OpenAI()
    print("처리 중입니다.")
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 이미지는 어디야, 그리고 무엇을 보여주고 있지?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{image_url}", 
                        }
                    },
                ],
            }
        ],
        max_tokens=1000,
    )
    return response.choices[0].message
if __name__ == '__main__':
    
    response=vison_talk( "https://www.jeju.go.kr/files/editor/4f81874a-321d-4926-a34e-c09cadd33fce.jpg" )
    print("="*100)
    print(response)

