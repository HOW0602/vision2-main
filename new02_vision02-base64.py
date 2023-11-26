import os
from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()  # openai_key .env 선언 사용
import dongsooAI as ds




def vison_talk( base64_image="" ):
    client = OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 이미지는 무엇을 보여주고 있지?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}", 
                        }
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message
 
if __name__ == '__main__':
    # print("image_url----------------------------------------------------------")
    # re=vison_talk( image_url="https://www.jeju.go.kr/files/editor/4f81874a-321d-4926-a34e-c09cadd33fce.jpg" )
    # print(re)

    print("image_file----------------------------------------------------------")
    base64_image=ds.image_tobase64_image("images/풍선2.png")
    re=vison_talk( base64_image=base64_image)
    print(re)


