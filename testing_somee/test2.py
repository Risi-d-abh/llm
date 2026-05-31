from openai import OpenAI

import os

from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display


load_dotenv(override=True)
api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print("No API key was found - please identify & fix!")
elif not api_key.startswith("gsk"):
    print("An API key was found, but it doesn't start gsk; please check you're using the right key")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them")
else:
    print("API key found and looks good so far!")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)

# Let's try out this utility

ed = fetch_website_contents("https://edwarddonner.com")
print(ed)