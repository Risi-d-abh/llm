from groq import Groq
from dotenv import load_dotenv
import os
import ollama

# Constants
MODEL_GROQ = "llama-3.3-70b-versatile"
MODEL_OLLAMA = "llama3.2"
 
# Setup
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Question
question = """
Please explain what this code does and why:

yield from {book.get("author") for book in books if book.get("author")}
"""

# GROQ Streaming
print("=== GROQ RESPONSE ===\n")

stream = client.chat.completions.create(
    model=MODEL_GROQ,
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

# OLLAMA
print("\n\n=== OLLAMA RESPONSE ===\n")

response = ollama.chat(
    model=MODEL_OLLAMA,
    messages=[
        {
            "role": "user",
            "content": question
        }
    ]
)

print(response["message"]["content"])