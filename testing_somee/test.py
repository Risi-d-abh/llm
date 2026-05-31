
import os

from dotenv import load_dotenv
#from scraper import fetch_website_contents
from IPython.display import Markdown, display
from google import genai


# Load environment variables in a file called .env

load_dotenv(override=True)
api_key = os.getenv('GEMINI_API_KEY')


# Check the key

if not api_key:
    print("No API key was found - please identify & fix!")
elif not api_key.startswith("AQ"):
    print("An API key was found, but it doesn't start AIzaSy...; please check you're using the right key")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them")
else:
    print("API key found and looks good so far!")
    
    
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Hello Gemini!"
)

print(response.text)




