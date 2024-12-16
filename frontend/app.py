# create a streamlit app that takes in a search prompt and returns a list of relevant events
# to run: streamlit run app.py

import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv  # Import dotenv


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
            output = semantics_search(client, data, classification_response["semantics"])
            st.write(output)



        if classification_response['keyword'] != '':
            st.write("Running Keyword Search")
            # perform a keyword search against all keywords from data
            keyword = classification_response['keyword']
            results = data[data['text'].str.contains(keyword, case=False, na=False)]
            st.write(results)

        if classification_response['location'] != '':
            st.write("Running Location Search")
            output = location_search(classification_response, data)

            results = data.head(5)
            st.write(results)
            
