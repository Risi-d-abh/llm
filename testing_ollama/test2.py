import os
from dotenv import load_dotenv
from openai import OpenAI
from scraper import fetch_website_contents


load_dotenv(override=True)

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

system_prompt=""" you are the type of assistant that likes to insult
the creative things in the website"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.

"""

def messages_for(website):
    return[
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_prompt_prefix+website}
    ]
    

def summarize(url):
    website=fetch_website_contents(url)
    response=client.chat.completions.create(
        model = "llama3.2",
        messages = messages_for(website)
    )
    return response.choices[0].message.content

print(summarize("https://www.thesouledstore.com"))