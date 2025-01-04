import os
import pandas as pd
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from googletrans import Translator

# Load environment variables from .env file
load_dotenv(r'C:\Users\swp\OneDrive\Desktop\MainCloass\rdr.env')
api_key = os.getenv("ApiKey")

# Configure the API with the API key
genai.configure(api_key=api_key)

# Initialize the Google Translator
translator = Translator()

# Load Burushaski data from your dataset
file_path = './Bb.xlsx'  # Ensure the file is in the same directory or update the path
burushaski_data = pd.read_excel(file_path)

# Rename columns for consistent reference
burushaski_data.columns = ['burushaski_phrase', 'english_translation']

def get_text_response(prompt):
    """Generate a text response using the Gemini API"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def translate_to_english(text):
    """Translate Burushaski text to English using the dataset"""
    # Check for exact matches in the dataset
    matching_row = burushaski_data[
        burushaski_data['burushaski_phrase'].str.contains(text, case=False, na=False)
    ]
    if not matching_row.empty:
        return matching_row['english_translation'].iloc[0]
    
    # Fallback to Google Translate if no match found
    try:
        translated = translator.translate(text, src='auto', dest='en')
        return translated.text
    except Exception as e:
        return f"Translation Error: {e}"

def suggest_words(text):
    """Suggest similar words from the dataset"""
    suggestions = []
    for word in burushaski_data['burushaski_phrase']:
        if word.lower().startswith(text.lower()[:2]):  # Match by first two characters
            suggestions.append(word)
    return suggestions

# Enhanced Streamlit UI
st.markdown(
    """
    <style>
    .main-title {
        color: #1E90FF;
        text-align: center;
        font-size: 40px;
        margin-top: 20px;
    }
    .subtitle {
        color: #4682B4;
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
    }
    .response-box, .translation-box, .suggestions-box {
        background-color: #F0F8FF;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .response-header, .translation-header, .suggestions-header {
        color: #5F9EA0;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">Burushaski to English ChatBot</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitle">Your companion for translating and learning!</h2>', unsafe_allow_html=True)

# User input
st.write("Type your sentence or words in Burushaski below, and let me handle the translation!")
user_input = st.text_input("Enter your text:", placeholder="e.g., Joolo Darang...")

if st.button("Ask"):
    if user_input:
        # Get translation and suggestions
        translation = translate_to_english(user_input)
        suggestions = suggest_words(user_input)
        response = get_text_response(translation)

        # Display translation
        st.markdown('<div class="translation-box">', unsafe_allow_html=True)
        st.markdown('<p class="translation-header">Translation:</p>', unsafe_allow_html=True)
        st.write(translation)
        st.markdown('</div>', unsafe_allow_html=True)

        # Display model response
        st.markdown('<div class="response-box">', unsafe_allow_html=True)
        st.markdown('<p class="response-header">Response:</p>', unsafe_allow_html=True)
        st.write(response)
        st.markdown('</div>', unsafe_allow_html=True)

        # Display suggestions if any
        if suggestions:
            st.markdown('<div class="suggestions-box">', unsafe_allow_html=True)
            st.markdown('<p class="suggestions-header">Suggestions:</p>', unsafe_allow_html=True)
            st.write(", ".join(suggestions))
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Please enter text to translate.")
