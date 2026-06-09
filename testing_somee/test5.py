# Let's try out this utility

import os
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display
from scraper import fetch_website_contents


load_dotenv(override=True)
# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."

client=OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

# Define our user prompt

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""
# See how this function creates exactly the format above

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]
    
    
# Try this out, and then try for a few more websites

#messages_for(ed)

# And now: call the OpenAI API. You will get very familiar with this!

def summarize(url):
    website = fetch_website_contents(url)
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = messages_for(website)
    )
    return response.choices[0].message.content

print(summarize("https://edwarddonner.com"))



# A function to display this nicely in the output, using markdown

"""def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))
    
print(display_summary("https://edwarddonner.com")) """