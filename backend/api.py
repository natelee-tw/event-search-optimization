from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import openai  # OpenAI's library for interacting with ChatGPT
import os
from dotenv import load_dotenv  # Import dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))


app = FastAPI()

# Request models
class SearchRequest(BaseModel):
    prompt: str

class ClassificationRequest(BaseModel):
    prompt: str

# Response models
class EventResponse(BaseModel):
    event: str
    location: str

class ClassificationResponse(BaseModel):
    classification: str
    confidence: float

def classify_search_prompt(prompt: str) -> Dict[str, str]:
    chat_prompt = f"""
    I need your help classifying search prompts into a JSON object. 

    For every input prompt, extract the following information:
    1. **Semantics**: The overall intent or theme of the prompt.
    2. **Keyword**: Any significant additional term or entity.
    3. **Location**: If the prompt mentions a geographic location.

    Always return a JSON object in this format:
    {{
      "semantics": "<semantic intent>",
      "keyword": "<significant keyword>",
      "location": "<location>"
    }}

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
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": chat_prompt}
            ]
        )
        classification = response["choices"][0]["message"]["content"].strip()
        return eval(classification)  # Convert string JSON to dictionary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with ChatGPT: {str(e)}")


# Mock functions for search logic
def mock_semantic_search(prompt: str) -> List[Dict[str, str]]:
    return [
        {"event": "Semantic Event 1", "location": "Location A"},
        {"event": "Semantic Event 2", "location": "Location B"},
    ]

def mock_location_search(prompt: str) -> List[Dict[str, str]]:
    return [
        {"event": "Location Event 1", "location": "Location C"},
        {"event": "Location Event 2", "location": "Location D"},
    ]

def mock_keyword_search(prompt: str) -> List[Dict[str, str]]:
    return [
        {"event": "Keyword Event 1", "location": "Location E"},
        {"event": "Keyword Event 2", "location": "Location F"},
    ]

def mock_genai_classification(prompt: str) -> Dict[str, str]:
    return {"classification": "semantic_search", "confidence": 0.95}

# Endpoints
@app.post("/semantics-search", response_model=List[EventResponse])
async def semantics_search(request: SearchRequest):
    results = mock_semantic_search(request.prompt)
    if not results:
        raise HTTPException(status_code=404, detail="No events found for the given prompt.")
    return results

@app.post("/location-search", response_model=List[EventResponse])
async def location_search(request: SearchRequest):
    results = mock_location_search(request.prompt)
    if not results:
        raise HTTPException(status_code=404, detail="No events found for the given prompt.")
    return results

@app.post("/keyword-search", response_model=List[EventResponse])
async def keyword_search(request: SearchRequest):
    results = mock_keyword_search(request.prompt)
    if not results:
        raise HTTPException(status_code=404, detail="No events found for the given prompt.")
    return results

@app.post("/genai-classification", response_model=ClassificationResponse)
async def genai_classification(request: ClassificationRequest):
    response = mock_genai_classification(request.prompt)
    if not response:
        raise HTTPException(status_code=500, detail="Failed to classify the prompt.")
    return response
