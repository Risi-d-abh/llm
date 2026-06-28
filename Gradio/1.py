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

system_message="You are a helpful assistant that responds in markdown without code blocks"

#system_message = "You are a helpful assistant"

"""def message_groq(prompt):
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
    response = groq.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages)
    return response.choices[0].message.content
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

def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()

#gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch()


"""message_input = gr.Textbox(label="Your message:", info="Enter a message to get info", lines=7)
message_output = gr.Textbox(label="Response:", lines=8)

view = gr.Interface(
    fn=message_gpt,
    title="your AI to assist you", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=["hello", "howdy"], 
    flagging_mode="never"
    )
view.launch()

"""

def stream_model(prompt, model):
    if model=="groq":
        result = stream_groq(prompt)
    elif model=="groq_2":
        result = stream_groq_2(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result
    
message_input = gr.Textbox(label="Your message:", info="Enter a message for the LLM", lines=7)
model_selector = gr.Dropdown(["groq", "groq_2"], label="Select model", value="groq")
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_model,
    title="LLMs", 
    inputs=[message_input, model_selector], 
    outputs=[message_output], 
    examples=[
            ["Explain the Transformer architecture to a layperson", "groq"],
            ["Explain the Transformer architecture to an aspiring AI engineer", "groq_2"]
        ], 
    flagging_mode="never"
    )
view.launch()

system_message = "You are a helpful assistant that responds in markdown without code blocks"
"""
message_input = gr.Textbox(label="Your message:", info="enter a msg for llama-3.3-70b-versatile", lines=7)
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_groq,
    title="GPT", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=[
        "Explain the Transformer architecture to a layperson",
        "Explain the Transformer architecture to an aspiring AI engineer",
        ], 
    flagging_mode="never"
    )
view.launch()
"""

