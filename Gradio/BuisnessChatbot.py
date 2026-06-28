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

system_message="You are a helpful assistant in a clothes store. You should try to gently encourage \
the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. \
For example, if the customer says 'I'm looking to buy a hat', \
you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales event.'\
Encourage the customer to buy hats if they are unsure what to get."

system_message += "\nIf the customer asks for shoes, you should respond that shoes are not on sale today, \
but remind the customer to look at hats!"

def chat(message,history):
    history=[{"role":h["role"],"content":h["content"]} for h in history]
    relevant_system_message=system_message
    if 'belt' in message.lower():
        relevant_system_message+=" The store does not sell belt; if you are asked for belt, be sure to point out other items on sale."
    messages=[{"role":"system", "content":relevant_system_message}]+history+[{"role":"user", "content":message}]
    stream=openai.chat.completions.create(model=model,messages=messages,stream=True)
    response=""
    for chunk in stream:
        response+=chunk.choices[0].delta.content or ''
        yield response
    


gr.ChatInterface(fn=chat).launch()