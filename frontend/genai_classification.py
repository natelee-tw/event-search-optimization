import requests


def classify_search_prompt(prompt):
    """Simulate a GenAI classification request"""
    # Here you would typically call a GenAI endpoint to classify the search prompt.
    # This is a mock response for illustration.
    
    # calls localhost:8000/genai-classification
    return requests.post("http://localhost:8000/genai-classification", json={"prompt": prompt})
