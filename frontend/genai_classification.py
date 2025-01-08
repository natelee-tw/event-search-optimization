from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from openai import OpenAI
import openai 
import os
from dotenv import load_dotenv  # Import dotenv
import json
import streamlit as st


class ClassificationRequest(BaseModel):
    prompt: str


class ClassificationResponse(BaseModel):
    semantics: str
    keyword: str
    location: str


app = FastAPI()

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)

def classify_search_prompt(prompt):
    print("prompt", prompt)
    response = call_openai_api(prompt)
    print("response", response)
    if not response:
        raise HTTPException(status_code=500, detail="Failed to classify the prompt.")
    return response


def call_openai_api(prompt):
    chat_prompt = f"""
    I need your help classifying search prompts into a JSON object. 

    For every input prompt, extract the following information:
    1. **Semantics**: The overall intent or theme of the prompt, only include activities or events or timing.
    2. **Keyword**: Any significant additional term or entity, could include event ID such as A1234, or any acronyms.
    3. **Location**: If the prompt mentions a geographic location or landmark in Singapore like xxx building, or 6 digits postal code like 123456.

    Always return a JSON object in this exact format:
    {{
      "semantics": "<semantic intent>",
      "keyword": "<significant keyword>",
      "location": "<location>"
    }}

    Do not include additional text or comments. If not in English, to translate to English.

    For example:
    Input: "Elderly Friendly events near Toa Payoh"
    Output: 
    {{
      "semantics": "elderly friendly",
      "keyword": "",
      "location": "Toa Payoh"
    }}

    Input: "Sporting for my primary school kids"
    Output:
    {{
      "semantics": "Sporting",
      "keyword": "Primary School",
      "location": ""
    }}

    Now, classify the following input:
    "{prompt}"
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": chat_prompt}
            ]
        )
        # Extract the content from the response
        raw_content = response.choices[0].message.content.strip()
        
        # Parse the JSON response
        response_data = json.loads(raw_content)
        print("response_data", response_data)
        
        # Validate using the Pydantic model
        validated_response = ClassificationResponse(**response_data)
        return validated_response
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format from ChatGPT.")
    except ValidationError as ve:
        raise HTTPException(status_code=500, detail=f"Validation Error: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with ChatGPT: {str(e)}")


    # return requests.post("http://localhost:8000/genai-classification", json={"prompt": prompt})
