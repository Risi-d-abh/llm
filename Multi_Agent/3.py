import os
import requests
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

load_dotenv(override=True)
groq_api_key=os.getenv("GROQ_API_KEY")

if groq_api_key:
    print(f"Groq api key exists and begins{groq_api_key[:4]}")
else:
    print("groq api key not set")
    
openai=OpenAI()

groq_url="https://api.groq.com/openai/v1"

groq=OpenAI(api_key=groq_api_key, base_url=groq_url)

alex="llama-3.3-70b-versatile"
harry="llama-3.1-8b-instant"
doue="llama-3.3-70b-versatile"

alex_sys="You are Alex, a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way.\
    you are in conversation with harry and doue "

harry_sys="You are harry, a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting.  you are in conversation with Alex and doue"

doue_sys="You are doue ,a very clever, foxy chatbot. you agree with everything even if the other person \
is very polite or argumentative but only to know about them and finally betraying them at last\
     you are in conversation with Alex and harry"


conversation = [
    {"speaker": "Alex", "text": "Hi everyone."},
    {"speaker": "Harry", "text": "Hello! Nice to meet you all."},
    {"speaker": "Doue", "text": "Hey friends."}
]

def call_bot(model,system_prompt):
    messages=[{"role":"system", "content":system_prompt}]
    
    history_text=""
    
    for msg in conversation:
        history_text+=f"{msg['speaker']}:{msg['text']}\n"
        
    
    messages.append({
        "role": "user",
        "content": f"""
Here is the conversation so far:

{history_text}

Continue the conversation with ONE response only.
"""
    })

    response = groq.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.8
    )

    return response.choices[0].message.content


for round_num in range(5):

    print(f"\n{'='*50}")
    print(f"ROUND {round_num + 1}")
    print(f"{'='*50}")

    # Alex speaks
    alex_reply = call_bot(alex, alex_sys)

    print(f"\nAlex:\n{alex_reply}")

    conversation.append({
        "speaker": "Alex",
        "text": alex_reply
    })

    # Harry speaks
    harry_reply = call_bot(harry, harry_sys)

    print(f"\nHarry:\n{harry_reply}")

    conversation.append({
        "speaker": "Harry",
        "text": harry_reply
    })

    # Doue speaks
    doue_reply = call_bot(doue, doue_sys)

    print(f"\nDoue:\n{doue_reply}")

    conversation.append({
        "speaker": "Doue",
        "text": doue_reply
    })
        
   
"""
def call_alex():
    messages=[{"role":"system", "content":alex_sys}]
    
    for assistant_msg, user_msg in zip(alex_messages,harry_messages):
        messages.append({"role":"assistant","content":assistant_msg})
        messages.append({"role":"user", "content":user_msg})
        
    response=groq.chat.completions.create(
        model=alex,
        messages=messages
    )
    
    return response.choices[0].message.content

def call_harry():
    messages=[{"role":"system", "content":harry_sys}]
    
    for assistant_msg, user_msg in zip(alex_messages,harry_messages):
        messages.append({"role":"user","content":user_msg})
        messages.append({"role":"assistant", "content":assistant_msg})
        
    messages.append({"role":"user","content":alex_messages[-1]})
    
    response=groq.chat.completions.create(
        model=harry,
        messages=messages
    )
    
    return response.choices[0].message.content

def call_doue():
    messages=[{"role":"system", "content":doue_sys}]
    
    for assistant_msg, user_msg in zip( doue_messages, harry_messages):
        messages.append({"role":"assistant", "content":assistant_msg})
        messages.append({"role":"user", "content":user_msg})
        
    messages.append({"role":"user", "content":harry_messages[-1]})
    
    response=groq.chat.completions.create(
        model=doue,
        messages=messages
    )
    
    return response.choices[0].message.content

for i in range(5):

    response1 = call_alex()
    print(f"\nArgumentative Bot: {response1}")

    alex_messages.append(response1)

    response2 = call_harry()
    print(f"\nPolite Bot: {response2}")

    harry_messages.append(response2)
    
    response3=call_doue()
    print(f"\nClever Bot: {response3}")
    
    """