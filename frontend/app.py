# create a streamlit app that takes in a search prompt and returns a list of relevant events
# to run: streamlit run app.py

import streamlit as st
import requests
import json

def classify_search_prompt(prompt):
    """Simulate a GenAI classification request"""
    # Here you would typically call a GenAI endpoint to classify the search prompt.
    # This is a mock response for illustration.
    
    # calls localhost:8000/genai-classification
    return requests.post("http://localhost:8000/genai-classification", json={"prompt": prompt})


def rerank_results(results):
    """Rerank search results (placeholder)"""
    # Implement reranking logic here. Currently returning results as is.
    return results

# Streamlit App Layout
st.title("HPB Event Search Application")
# add a health promotion board logo
# make the logo smaller
st.image("frontend/h365.png", width=120)

st.markdown("Search for events based on your input prompt.")

# Input field for search prompt
search_prompt = st.text_input("Enter your search prompt:", placeholder="Type something like 'elderly friendly events near toa payoh'")

if st.button("Search"):
    if not search_prompt.strip():
        st.error("Please enter a search prompt to proceed.")
    else:
        # Classify search prompt using GenAI
        with st.spinner("Classifying your search prompt..."):
            classification_response = classify_search_prompt(search_prompt).json()
            print(classification_response)

        st.write(f"Classification: {classification_response}")

        if classification_response['semantics'] != '':
            st.write("Running Semantics Search")

        if classification_response['keyword'] != '':
            st.write("Running Keyword Search")

        if classification_response['location'] != '':
            st.write("Running Location Search")

