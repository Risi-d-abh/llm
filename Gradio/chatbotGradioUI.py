import os
from dotenv import load_dotenv
import gradio as gr
from groq import Groq
from openai import OpenAI

load_dotenv(override=True)
api_key=os.getenv('GROQ_API_KEY')

if api_key:
    print(f"api key exists and begins with {api_key[:8]}")
else:
    print("api key not set")
    
openai=Groq()
model='llama-3.1-8b-instant'

system_message='you are a helpful assistant'

def chat(message,history):
    history=[{"role":h["role"],"content":h["content"]} for h in history]
    messages=[{"role":"system", "content":system_message}]+history+[{"role":"user", "content":message}]
    stream=openai.chat.completions.create(model=model,messages=messages,stream=True)
    response=""
    for chunk in stream:
        response+=chunk.choices[0].delta.content or ''
        yield response
    


gr.ChatInterface(fn=chat).launch()