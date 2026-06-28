from scraper import fetch_website_contents
import os
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq
import gradio as gr



load_dotenv(override=True)
groq_api_key=os.getenv('GROQ_API_KEY')

if groq_api_key:
    print(f"groq API Key exists and begins {groq_api_key[:8]}")
else:
    print("groq API Key not set")
    
openai=OpenAI()

groq_url="https://api.groq.com/openai/v1"

groq=OpenAI(api_key=groq_api_key, base_url=groq_url)


system_message = """
You are an assistant that analyzes the contents of a company website landing page
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
"""


def stream_groq(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = groq.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result
        
def stream_groq_2(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = groq.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


def stream_brochure(company_name, url, model):
    yield ""
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    prompt += fetch_website_contents(url)
    if model=="groq":
        result = stream_groq(prompt)
    elif model=="groq_2":
        result = stream_groq_2(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result
    
name_input = gr.Textbox(label="Company name:")
url_input = gr.Textbox(label="Landing page URL including http:// or https://")
model_selector = gr.Dropdown(["groq", "groq_2"], label="Select model", value="groq")
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_brochure,
    title="Brochure Generator", 
    inputs=[name_input, url_input, model_selector], 
    outputs=[message_output], 
    examples=[
            ["Hugging Face", "https://huggingface.co", "groq"],
            ["Edward Donner", "https://edwarddonner.com", "groq_2"]
        ], 
    flagging_mode="never"
    )
view.launch()