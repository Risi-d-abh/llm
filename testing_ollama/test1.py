from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="gemma3:270m",
    messages=[
        {"role": "user", "content": "Explain APIs"}
    ]
)

print(response.choices[0].message.content)