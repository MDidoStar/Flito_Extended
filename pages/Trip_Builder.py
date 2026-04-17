# Importing libraries
import io
import re
import pandas as pd
import google.generativeai as genai
import speech_recognition as sr
import streamlit as st
from datetime import date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from color import edit 
st.set_page_config(page_title="FLITO: Trip Builder", page_icon='logo.png', layout="wide")

genai.configure(api_key=st.secrets["gemini_api_key"])
model = genai.GenerativeModel('gemini-2.5-flash')

edit()

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('countries.csv')
        df['Country'] = df['Country'].astype(str)
        df['City'] = df['City'].astype(str)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Country', 'City', 'Currency_Code'])

df = load_data()

def get_countries():
    return sorted(df['Country'].unique().tolist()) if not df.empty else []

def get_cities(country):
    if not df.empty and country:
        return sorted(df[df['Country'] == country]['City'].unique().tolist())
    return []

def transcribe_audio(audio_file):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="en-US")
            return text
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"Error processing audio: {e}"

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def convert_markdown_to_html(text):
    text = escape_html(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'\[(.+?)\]\((https?://[^\)]+)\)', r'<a href="\2" color="blue">\1</a>', text)
    text = re.sub(r'(?<!href=")(https?://[^\s<>"]+)', r'<a href="\1" color="blue">\1</a>', text)
    return text

def generate_pdf_from_text(text_content):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1a1a1a'), spaceAfter=14, spaceBefore=10, leading=20)
    heading2_style = ParagraphStyle('CustomHeading2', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#2c3e50'), spaceAfter=10, spaceBefore=8, leading=16, leftIndent=10)
    heading3_style = ParagraphStyle('CustomHeading3', parent=styles['Heading3'], fontSize=11, textColor=colors.HexColor('#34495e'), spaceAfter=8, spaceBefore=6, leading=14, leftIndent=15)
    bold_style = ParagraphStyle('BoldText', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#2c3e50'), spaceAfter=6, leading=14, leftIndent=20)
    normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, spaceAfter=6, leading=14, leftIndent=20)
    bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], fontSize=10, spaceAfter=4, leading=14, leftIndent=35, bulletIndent=25)
    lines = text_content.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped: story.append(Spacer(1, 8)); i += 1; continue
        if '|' in stripped and i + 1 < len(lines) and '|' in lines[i + 1]:
            table_data = []
            while i < len(lines) and '|' in lines[i].strip():
                row = lines[i].strip()
                if re.match(r'^[\|\s\-:]+$', row): i += 1; continue
                cells = [cell.strip() for cell in row.split('|') if cell]
                if cells: table_data.append(cells)
                i += 1
            if table_data:
                t = Table(table_data, hAlign='CENTER')
                t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#3498db')),('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),('ALIGN',(0,0),(-1,-1),'CENTER'),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,0),10),('BOTTOMPADDING',(0,0),(-1,0),12),('BACKGROUND',(0,1),(-1,-1),colors.beige),('GRID',(0,0),(-1,-1),0.5,colors.grey),('FONTNAME',(0,1),(-1,-1),'Helvetica'),('FONTSIZE',(0,1),(-1,-1),9)]))
                story.append(Spacer(1,8)); story.append(t); story.append(Spacer(1,12))
            continue
        if stripped.startswith('###'): story.append(Paragraph(convert_markdown_to_html(stripped.replace('###','').strip()), heading3_style))
        elif stripped.startswith('##'): story.append(Paragraph(convert_markdown_to_html(stripped.replace('##','').strip()), heading2_style))
        elif stripped.startswith('#'): story.append(Paragraph(convert_markdown_to_html(stripped.replace('#','').strip()), title_style))
        elif stripped.startswith('**') and stripped.endswith('**'): story.append(Paragraph(f'<b>{escape_html(stripped.replace("**","").strip())}</b>', bold_style))
        elif stripped.startswith(('*','- ')): story.append(Paragraph(f'• {convert_markdown_to_html(stripped.lstrip("*-").strip())}', bullet_style))
        elif re.match(r'^\d+\.', stripped): story.append(Paragraph(convert_markdown_to_html(stripped), bold_style))
        else: story.append(Paragraph(convert_markdown_to_html(stripped), normal_style))
        i += 1
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

with st.sidebar:
    st.logo(image='logo.png', size='large', icon_image='logo.png')
#    st.subheader('Would you like to go Premium?')
#    st.link_button('Subscribe now!', 'https://buy.stripe.com/test_3cIcN592b5iLfN93mU8so00')
    if st.button("← Back to FLITO", key="back_btn"):
        st.switch_page("FLITO.py")

st.title("✈️ Trip Builder (Premium)")
st.write("Get a complete day-by-day itinerary tailored to your dates and budget.")

countries_list = get_countries()

st.subheader("Step 1: Trip Mode")
with st.container():
    trip_type = st.segmented_control(
        "Select Trip Mode",
        options=["One City", "Multiple Cities"],
        default="One City",
        key="trip_mode_segment"
    )

    st.subheader("Step 2: Trip Details")
    col1, col2 = st.columns(2)
    with col1:
        trip_dest_country = st.selectbox("Destination Country", countries_list, key="trip_country")
        trip_start_date = st.date_input("Start Date", min_value=date.today())
        trip_budget = st.number_input("Total Trip Budget:", min_value=100, value=1000)
    with col2:
        if trip_type == "One City":
            tb_cities = get_cities(trip_dest_country)
            trip_dest_city = st.selectbox("Destination City", tb_cities, key="trip_city")
        else:
            st.info("🗺️ AI will distribute your trip across the best cities.")
            trip_dest_city = "Multiple Cities"
        trip_end_date = st.date_input("End Date", min_value=date.today())

    st.subheader("Step 3: Preferences")
    input_mode = st.radio("How would you like to input preferences?", ["Text", "Voice AI (English)"], horizontal=True)

    trip_extra_req = ""
    if input_mode == "Text":
        trip_extra_req = st.text_area("Any specific preferences? (e.g. Vegetarian food, love museums, hate hiking)")
    else:
        audio_value = st.audio_input("Record your preferences (Click microphone)")
        if audio_value:
            with st.spinner("Transcribing your voice..."):
                transcribed_text = transcribe_audio(audio_value)
                st.success(f"Heard: {transcribed_text}")
                trip_extra_req = transcribed_text

    if st.button("Generate Plan!"):
        valid_input = (trip_dest_country and trip_start_date and trip_end_date)
        if trip_type == "One City" and not trip_dest_city:
            valid_input = False
        if valid_input:
            if trip_end_date < trip_start_date:
                st.error("End date cannot be before start date.")
            else:
                delta = trip_end_date - trip_start_date
                num_days = delta.days
                user = st.session_state.get("logged_in_user")
                prefs = user.get("preferences", {}) if user else {}
                if trip_type == "One City":
                    location_context = f"to {trip_dest_city}, {trip_dest_country}"
                else:
                    location_context = f"touring multiple cities in {trip_dest_country}. Please distribute these {num_days} days logically across the best cities in this country."
                prompt = f"""
                    I will travel from {trip_start_date} to {trip_end_date} ({num_days} days) {location_context}.
                    My budget is {trip_budget} USD.
                    The date of travel is crucial to identify if it's in winter or summer, so the activities must differ based on the season of the dates provided.
                    Recommend hotels/stays by stating:
                    1. Hotel name (If multiple cities, suggest one for each city)
                    2. Address
                    3. Price list of stay in a table
                    4. Contact phone number
                    5. Website (If available)
                    AND
                    Please generate a detailed trip plan for EACH day (Day 1 to Day {num_days}).
                    For each day, you must include specific recommendations for:
                    1. Food (Mention specific restaurants to try and cafes)
                    2. Activities and tourism places (Appropriate for the season/weather)
                    3. Shopping malls or areas
                    Extra preferences: {trip_extra_req}
                    {f'''
                    The user also has these saved travel preferences, incorporate them throughout the plan:
                    - Language: {prefs.get("language", "English")}
                    - Budget style: {prefs.get("budget", "Moderate")}
                    - Food preference: {prefs.get("food", "No preference")}
                    - Travel style: {prefs.get("travel_style", "Explorer")}
                    - Favorite activity: {prefs.get("activity", "Sightseeing")}
                    - Preferred transport: {prefs.get("transport", "Any")}
                    ''' if prefs else ''}
                    Format the output clearly by Day (e.g., **Day 1: [Date] - [City Name]**).
                    Make the response brief for each day, keep it simple and very readable.
                    """
                with st.spinner(f"Building your {num_days}-day plan for {trip_dest_country}..."):
                    response = model.generate_content(prompt)
                    st.write(response.text)
                    pdf_content = generate_pdf_from_text(response.text)
                    st.download_button(label='Download Plan PDF ⬇️', data=pdf_content, file_name=f'{trip_dest_country}_trip.pdf', mime="application/pdf")
        else:
            st.warning("Please fill in all destination and date fields.")

st.write('---')
st.caption('🌟 AI-powered trip planning using Google Gemini')
