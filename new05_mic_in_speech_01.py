import os
from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()  # openai_key .env 선언 사용
import dongsooAI as ds
from openai import OpenAI

client = OpenAI()

prompt=[]


while True:
    query=input(" query = ")
    if query=="":
       break
     
    prompt.append({"role": "user", "content": query } )    
        
    response  = client.chat.completions.create(
                                model="gpt-4-vision-preview",
                                messages=prompt,
                                 max_tokens=1000,
                                ) 
    ans=response.choices[0].message.content 

    prompt.append({"role": "assistant", "content": ans } )    
    print( "  ans = ",ans ,"\n" )