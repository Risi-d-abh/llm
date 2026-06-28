import os
import json
import time
import sqlite3
import requests
import gradio as gr

from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

from groq import Groq
from elevenlabs.client import ElevenLabs

load_dotenv(override=True)

groq_api_key = os.getenv("GROQ_API_KEY")
flux_api_key = os.getenv("FLUX_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

if groq_api_key:
    print(f"Groq API Loaded : {groq_api_key[:8]}")
else:
    print("Groq API Key Missing")

if flux_api_key:
    print(f"Flux API Loaded : {flux_api_key[:8]}")
else:
    print("Flux API Key Missing")

if elevenlabs_api_key:
    print(f"ElevenLabs Loaded : {elevenlabs_api_key[:8]}")
else:
    print("ElevenLabs API Key Missing")


MODEL = "llama-3.3-70b-versatile"

groq = Groq(api_key=groq_api_key)

eleven = ElevenLabs(
    api_key=elevenlabs_api_key
)

DB = "flight.db"

system_message = """
You are FlightAI.

You are a polite Airline Assistant.

Keep answers under one sentence.

Whenever the user asks about ticket prices,
always use the available tool.

Be accurate.
"""

def get_ticket_price(destination_city):

    print(f"DATABASE TOOL CALLED : {destination_city}")

    with sqlite3.connect(DB) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT price
            FROM tickets
            WHERE city=?
            """,
            (destination_city.lower(),)
        )

        result = cursor.fetchone()

    if result:

        return f"The ticket price to {destination_city} is ${result[0]}."

    return f"Sorry, no ticket price is available for {destination_city}."

price_function = {

    "name": "get_ticket_price",

    "description":
        "Get the return ticket price for a city.",

    "parameters": {

        "type": "object",

        "properties": {

            "destination_city": {

                "type": "string",

                "description":
                "Destination city"

            }

        },

        "required": [

            "destination_city"

        ],

        "additionalProperties": False

    }

}

tools = [

    {

        "type": "function",

        "function": price_function

    }

]

def artist(city):

    print(f"Generating image for {city}")

    generate_url = (
        "https://api.fluxapi.ai/api/v1/flux/kontext/generate"
    )

    record_url = (
        "https://api.fluxapi.ai/api/v1/flux/kontext/record-info"
    )

    headers = {

        "Authorization": f"Bearer {flux_api_key}",

        "Content-Type": "application/json"

    }

    payload = {

        "model": "flux-kontext-pro",

        "prompt":
        f"""
        A beautiful travel poster of {city},
        vibrant colors,
        famous landmarks,
        tourism,
        pop art,
        ultra detailed
        """

    }

    response = requests.post(

        generate_url,

        headers=headers,

        json=payload

    )

    response.raise_for_status()

    task_id = response.json()["data"]["taskId"]

    print("Task Created :", task_id)

    while True:

        status = requests.get(

            record_url,

            headers=headers,

            params={

                "taskId": task_id

            }

        )

        status.raise_for_status()

        data = status.json()["data"]

        if data["successFlag"] == 1:

            image_url = data["response"]["resultImageUrl"]

            print("Image Ready")

            image = requests.get(image_url)

            return Image.open(
                BytesIO(image.content)
            )

        elif data["successFlag"] == 3:

            raise Exception(
                data["errorMessage"]
            )

        print("Waiting for image...")

        time.sleep(2)

def talker(text):

    audio = eleven.text_to_speech.convert(

        voice_id="JBFqnCBsd6RMkjVDRZzb",

        model_id="eleven_multilingual_v2",

        text=text

    )

    filename = "speech.mp3"

    with open(filename, "wb") as f:

        for chunk in audio:

            f.write(chunk)

    return filename

def handle_tool_calls_and_return_cities(message):

    responses = []
    cities = []

    for tool_call in message.tool_calls:

        if tool_call.function.name == "get_ticket_price":

            arguments = json.loads(
                tool_call.function.arguments
            )
            print(arguments)

            city = arguments.get(
                "destination_city"
            )

            cities.append(city)
            
            print(city)

            tool_result = get_ticket_price(city)

            responses.append({

                "role": "tool",

                "tool_call_id": tool_call.id,

                "content": tool_result

            })

    return responses, cities

def chat(history):

    history = [
        {
            "role": h["role"],
            "content": h["content"]
        }
        for h in history
    ]

    messages = [

        {
            "role": "system",
            "content": system_message
        }

    ] + history

    response = groq.chat.completions.create(

        model=MODEL,

        messages=messages,

        tools=tools

    )

    cities = []
    image = None

    while response.choices[0].finish_reason == "tool_calls":

        assistant_message = response.choices[0].message

        tool_responses, cities = (
            handle_tool_calls_and_return_cities(
                assistant_message
            )
        )

        messages.append(assistant_message)

        messages.extend(tool_responses)

        response = groq.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=tools

        )

    reply = response.choices[0].message.content

    history.append({

        "role": "assistant",

        "content": reply

    })

    print("Generating Speech...")

    voice = talker(reply)

    if cities:

        try:

            print("Generating Image...")

            image = artist(cities[0])

        except Exception as e:

            print(e)

            image = None

    return history, voice, image

def put_message_in_chatbot(message, history):

    history = history + [

        {

            "role": "user",

            "content": message

        }

    ]

    return "", history

with gr.Blocks(title="FlightAI") as ui:

    gr.Markdown("FlightAI")

    with gr.Row():

        chatbot = gr.Chatbot(

            height=520,

            

        )

        image_output = gr.Image(

            height=520,

            interactive=False,

            label="Destination"

        )

    audio_output = gr.Audio(

        autoplay=True,

        label="Assistant Voice"

    )

    message = gr.Textbox(

        label="Ask FlightAI",

        placeholder="Example: Ticket price for Paris"

    )

    message.submit(

        put_message_in_chatbot,

        inputs=[

            message,

            chatbot

        ],

        outputs=[

            message,

            chatbot

        ]

    ).then(

        chat,

        inputs=chatbot,

        outputs=[

            chatbot,

            audio_output,

            image_output

        ]

    )

ui.launch(
    inbrowser=True,
    auth=("rishabh", "pwdNED")
)