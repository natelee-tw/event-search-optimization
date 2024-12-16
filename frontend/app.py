# create a streamlit app that takes in a search prompt and returns a list of relevant events
# to run: streamlit run app.py

import streamlit as st
import requests
import json

def classify_search_prompt(prompt):
    """Simulate a GenAI classification request"""
    # Here you would typically call a GenAI endpoint to classify the search prompt.
    # This is a mock response for illustration.
    return {
        "classification": "semantic_search",
        "confidence": 0.95
    }

def perform_search(classification, prompt):
    """Perform search based on the classification"""
    # Replace this with actual search API calls
    if classification == "semantic_search":
        return [{"event": "Semantic Search Event 1", "location": "Location A"},
                {"event": "Semantic Search Event 2", "location": "Location B"}]
    elif classification == "location_search":
        return [{"event": "Location-Based Event 1", "location": "Location C"},
                {"event": "Location-Based Event 2", "location": "Location D"}]
    elif classification == "keyword_search":
        return [{"event": "Keyword Event 1", "location": "Location E"},
                {"event": "Keyword Event 2", "location": "Location F"}]
    return []

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
            classification_response = classify_search_prompt(search_prompt)
            classification = classification_response.get("classification")
            confidence = classification_response.get("confidence")

        st.write(f"Classification: {classification} (Confidence: {confidence:.2f})")

        # Perform search based on classification
        with st.spinner("Performing search..."):
            results = perform_search(classification, search_prompt)

        # Rerank results
        reranked_results = rerank_results(results)

        # Display results
        st.subheader("Search Results")
        if reranked_results:
            for idx, result in enumerate(reranked_results, start=1):
                st.write(f"{idx}. **Event**: {result['event']}  **Location**: {result['location']}")
        else:
            st.warning("No events found for your search prompt.")
