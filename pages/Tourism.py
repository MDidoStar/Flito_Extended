# Importing libraries
import io
import re
import pandas as pd
import google.generativeai as genai
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from color import edit
st.set_page_config(page_title="FLITO: Tourism", page_icon='logo.png', layout="wide")

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
    output_number = st.slider("How many outputs shall I suggest?:", 1, 10, 1, key="output_num")
    st.divider()
    if st.button("← Back to FLITO", key="back_btn"):
        st.switch_page("FLITO.py")

st.title("🏝️ Tourism")
st.write("Discover Tourist Attractions!")

countries_list = get_countries()

col1, col2 = st.columns(2)
with col1:
    attraction_type = st.selectbox('Type of attraction', ['Museum', 'Historical Site', 'Natural Wonder', 'Theme Park', 'Monument', 'Beach', 'Temple/Religious Site'], key='tourism_type')
    tourist_country = st.selectbox('Country', countries_list, key='tourist_country')
    tourist_rating = st.slider('Min Rating', 1, 5, 3, key='tourist_rating')
with col2:
    activity_preference = st.selectbox('Activity preference', ['Sightseeing', 'Adventure', 'Relaxation', 'Cultural Experience', 'Photography', 'Family Fun'], key='tourism_activity')
    t_cities = get_cities(tourist_country)
    tourist_city = st.selectbox('City', t_cities, key='tourist_city')
    tourist_price = st.selectbox('Cost', ['Free', 'Budget-friendly', 'Moderate', 'Premium'], key='tourist_price')

st.write('---')
tourist_extra = st.text_area('Extra details (optional)', key='tourist_extra')

if st.button('Discover now', key='tourist_search'):
    if not tourist_city or not tourist_country:
        st.error("Please select both a country and a city.")
    else:
        user = st.session_state.get("logged_in_user")
        prefs = user.get("preferences", {}) if user else {}
        pref_context = ""
        if prefs:
            pref_context = f"""
            The user has the following personal preferences, please tailor your answer to them:
            - Language preference: {prefs.get('language', 'English')}
            - Budget style: {prefs.get('budget', 'Moderate')}
            - Travel style: {prefs.get('travel_style', 'Explorer')}
            - Favorite activity: {prefs.get('activity', 'Sightseeing')}
            """
        prompt = f"""
            Suggest for me {attraction_type} tourist attractions for {activity_preference} in {tourist_city}, {tourist_country}.
            The places should have a minimum rating of {tourist_rating} stars or more, be {tourist_price}.
            Give me {output_number} options to consider with the following details for each:
            1. Name of the attraction
            2. Address
            3. Rating (out of 5)
            4. Entry fees/ticket prices in a table format if available
            5. Best time to visit
            6. Main highlights and activities
            7. Brief description
            8. Contact information and opening hours
            9. Tips for visitors
            Extra notes: {tourist_extra}
            {pref_context}
            Please format the response clearly with each attraction as a separate section.
            Make your answer short and focused only on what I requested.
            """
        with st.spinner('Discovering attractions...'):
            response = model.generate_content(prompt)
            st.write(response.text)
            pdf_content = generate_pdf_from_text(response.text)
            st.download_button(label='Download PDF ⬇️', data=pdf_content, file_name='tourist_recommendations.pdf', mime="application/pdf")

st.write('---')
st.caption('🌟 AI-powered recommendations using Google Gemini')
