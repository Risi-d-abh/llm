import os
import json
from dotenv import load_dotenv
from scraper import fetch_website_links, fetch_website_contents
from groq import Groq

load_dotenv(override=True)
api_key=os.getenv('GROQ_API_KEY')

if api_key and api_key.startswith('gsk') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key")
    
MODEL="llama-3.3-70b-versatile"
groq = Groq()


link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""

def get_links_user_prompt(url):
    user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company, 
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt

def select_relevant_links(url):
    print(f"Selecting relevant links for {url} by calling {MODEL}")
    response = groq.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)}
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    print(f"Found {len(links['links'])} relevant links")
    return links


def fetch_page_and_all_relevant_links(url):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result

marketing_strategy_system_prompt = """
You are a senior marketing strategist.

Your task is to analyze company information and create a marketing strategy report.

Identify:

1. Company Overview
2. Target Audience
3. Customer Pain Points
4. Unique Selling Propositions (USPs)
5. Key Benefits of Products/Services
6. Brand Positioning
7. Marketing Angles
8. Sales Messaging

Focus on information useful for creating a persuasive sales brochure.

Respond in markdown format.
"""

def get_marketing_strategy_user_prompt(company_name, url):

    user_prompt = f"""
You are analyzing a company called: {company_name}

Below is information collected from the company website,
including its homepage and other important pages.

Analyze the company and generate a marketing strategy report.

Website Information:

"""

    user_prompt += fetch_page_and_all_relevant_links(url)

    user_prompt = user_prompt[:7000]

    return user_prompt

def create_marketing_strategy(company_name, url):

    print(f"Creating marketing strategy for {company_name}")

    response = groq.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": marketing_strategy_system_prompt
            },
            {
                "role": "user",
                "content": get_marketing_strategy_user_prompt(
                    company_name,
                    url
                )
            }
        ]
    )

    return response.choices[0].message.content

brochure_system_prompt = """
You are an expert marketing copywriter.

Your task is to create a professional sales brochure.

The brochure should include:

- Company Overview
- Products and Services
- Unique Selling Propositions
- Customer Benefits
- Brand Positioning
- Call to Action

Write in a persuasive and professional tone.

Respond in markdown without code blocks.
"""

def get_brochure_user_prompt(company_name, url):

    marketing_strategy = create_marketing_strategy(
        company_name,
        url
    )

    user_prompt = f"""
You are creating a professional sales brochure for:

{company_name}

Below is a marketing strategy report prepared by a marketing strategist.

{marketing_strategy}

Use this information to create a persuasive sales brochure.

Respond in markdown.
"""

    return user_prompt


def stream_brochure(company_name, url):

    stream = groq.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": brochure_system_prompt
            },
            {
                "role": "user",
                "content": get_brochure_user_prompt(
                    company_name,
                    url
                )
            }
        ],
        stream=True
    )

    response = ""

    for chunk in stream:

        content = (
            chunk.choices[0]
            .delta.content or ""
        )

        response += content

        print(
            content,
            end="",
            flush=True
        )

    return response

        
print(stream_brochure("HuggingFace", "https://huggingface.co"))