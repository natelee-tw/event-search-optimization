# create a streamlit app that takes in a search prompt and returns a list of relevant events
# to run: streamlit run app.py

import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv


from genai_classification import classify_search_prompt
from location_search import location_search
from semantics_search import semantics_search


# Streamlit App Layout
st.title("HPB Event Search Application")
st.image("frontend/h365.png", width=120)

st.markdown("Search for events based on your input prompt.")

# Input field for search prompt
search_prompt = st.text_input("Enter your search prompt:", placeholder="Type something like 'elderly friendly events near toa payoh'")

# get lat and long of all data
data = pd.read_pickle("data/embedded_activities_lat_lon.pkl")

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

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
            semantics_output = semantics_search(client, data, classification_response["semantics"])
            st.write(semantics_output[["Event ID", "Activity", "Time", "Location", "score_semantics"]])

        if classification_response['keyword'] != '':
            st.write("Running Keyword Search")
            # perform a keyword search against all keywords from data
            keyword = classification_response['keyword']
            keyword_output = data[data['text'].str.contains(keyword, case=False, na=False)]
            keyword_output["score_keyword"] = 2
            st.write(keyword_output[["Event ID", "Activity", "Time", "Location", "score_keyword"]])

        if classification_response['location'] != '':
            st.write("Running Location Search")
            location_output = location_search(classification_response, data)

            st.write(location_output[["Event ID", "Activity", "Time", "Location", "score_location"]])

        # combining all outputs
        data_combined = data.copy()
        data_combined['score'] = 0

        st.write("Combining All Searches and Reranking")

        if classification_response['semantics'] != '':
            data_combined = data_combined.merge(semantics_output[["score_semantics"]], left_index=True, right_index=True, how='left')
            data_combined['score_semantics'] = data_combined['score_semantics'].fillna(0)
            data_combined['score'] += data_combined['score_semantics']
        if classification_response['keyword'] != '':
            data_combined = data_combined.merge(keyword_output[["score_keyword"]], left_index=True, right_index=True, how="left")
            data_combined['score_keyword'] = data_combined['score_keyword'].fillna(0)
            data_combined['score'] += data_combined['score_keyword']
        if classification_response['location'] != '':
            data_combined = data_combined.merge(location_output[["score_location"]], left_index=True, right_index=True, how="left")
            data_combined['score_location'] = data_combined['score_location'].fillna(0)
            data_combined['score'] += data_combined['score_location']

        data_combined = data_combined.sort_values(by='score', ascending=False)

        columns_to_display = ['text', 'score', 'score_semantics', 'score_keyword', 'score_location']
        existing_columns = [col for col in columns_to_display if col in data_combined.columns]
        st.write(data_combined[existing_columns].head(30))        

            
