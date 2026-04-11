# Importing libraries
import google.generativeai as genai
import streamlit as st
from color import edit
st.set_page_config(page_title="FLITO: Translation", page_icon='logo.png', layout="wide")

genai.configure(api_key=st.secrets["gemini_api_key"])
model = genai.GenerativeModel('gemini-2.5-flash')

edit()

languages = [
    "English", "Chinese", "Hindi", "Spanish", "Arabic", "French", "Greek", "Swedish", "Dutch",
    "Bengali", "Portuguese", "Russian", "Indonesian", "Urdu", "German", "Japanese",
    "Nigerian Pidgin", "Marathi", "Telugu", "Turkish", "Hausa", "Tamil", "Estonian",
    "Yue Chinese (Cantonese)", "Western Punjabi", "Swahili", "Tagalog", "Wu Chinese", "Iranian Persian",
    "Korean", "Thai", "Italian", "Gujarati", "Amharic", "Kannada", "Bhojpuri",
    "Polish", "Ukrainian", "Malayalam", "Odia", "Uzbek", "Sindhi", "Romanian", "Chittagonian",
    "Igbo", "Northern Pashto", "South Azerbaijani", "Saraiki", "Nepali", "Sinhalese",
    "Zhuang", "Somali", "Belarusian", "Czech", "Zulu"
]

with st.sidebar:
    st.logo(image='logo.png', size='large', icon_image='logo.png')
    st.divider()
    if st.button("← Back to FLITO", key="back_btn"):
        st.switch_page("E:\Coding Mohamed\Flito Extened\Flito-main\FLITO.py")

st.title("🗣️ Translation")
st.write("Translate Any Language!")

col1, col2 = st.columns(2)
with col1:
    From_Language = st.selectbox('From Which Language', options=languages, key='From_lang')
with col2:
    To_Language = st.selectbox("To which Language", options=languages, key="To_lang")

st.write('---')
The_Word = st.text_area("Enter the sentence you need to translate:", key="which_word")

if st.button('Translate now', key='Translate_search'):
    prompt = f"""
        I need the translation of the following word "{The_Word}" from the {From_Language} language to the {To_Language} language.
        Please format the response clearly with the word and its pronunciation only.
        1. Meaning:
        2. Pronunciation:
        Make your answer short and focused only on what I requested.
        """
    with st.spinner('Translating the sentence...'):
        response = model.generate_content(prompt)
        st.write(response.text)

st.write('---')
st.caption('🌟 AI-powered translation using Google Gemini')
