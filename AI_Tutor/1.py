import os
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

load_dotenv(override=True)
api_key = os.getenv('GROQ_API_KEY')


if api_key and api_key.startswith('gsk_') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key")
    

MODEL = 'llama-3.3-70b-versatile'
client = Groq()

groq_url="https://api.groq.com/openai/v1"

groq = OpenAI(api_key=api_key, base_url=groq_url)


question = """
Please explain what this code does and why:
yield from {book.get("author") for book in books if book.get("author")}
"""




stream = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": question}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")




    

  