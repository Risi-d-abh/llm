
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')


if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if groq_api_key:
    print(f"Groq API Key exists and begins {groq_api_key[:4]}")
else:
    print("Groq API Key not set (and this is optional)")

    
openai = OpenAI()

groq_url = "https://api.groq.com/openai/v1"


groq = OpenAI(api_key=groq_api_key, base_url=groq_url)


groq_model="llama-3.3-70b-versatile"
groq_model_2="llama-3.1-8b-instant"

groq_system= "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

groq_2_system= "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

groq_messages=["hi there"]
groq_2_messages=["hi"]

def call_groq():
    messages = [{"role": "system", "content": groq_system}]

    for assistant_msg, user_msg in zip(groq_messages, groq_2_messages):
        messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": user_msg})

    response = groq.chat.completions.create(
        model=groq_model,
        messages=messages
    )

    return response.choices[0].message.content


def call_groq_2():
    messages = [{"role": "system", "content": groq_2_system}]

    for assistant_msg, user_msg in zip(groq_messages, groq_2_messages):
        messages.append({"role": "user", "content": assistant_msg})
        messages.append({"role": "assistant", "content": user_msg})

    messages.append({"role": "user", "content": groq_messages[-1]})

    response = groq.chat.completions.create(
        model=groq_model_2,
        messages=messages
    )

    return response.choices[0].message.content

for i in range(5):

    response1 = call_groq()
    print(f"\nArgumentative Bot: {response1}")

    groq_messages.append(response1)

    response2 = call_groq_2()
    print(f"\nPolite Bot: {response2}")

    groq_2_messages.append(response2)




