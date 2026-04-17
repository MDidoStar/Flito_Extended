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
st.set_page_config(page_title="FLITO: Shopping", page_icon='logo.png', layout="wide")

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

st.title("🛍️ Shopping")
st.write("Shop til you drop! Find the best malls, stores, and markets.")

countries_list = get_countries()

col1, col2 = st.columns(2)
with col1:
    shop_country = st.selectbox("Country", countries_list, key="shop_country")
    shop_type = st.selectbox("Type of Shopping", ["Shopping Mall", "Outlet", "Local Market", "Boutique", "Souvenir Shop", "Street Market"], key="shop_type")
with col2:
    s_cities = get_cities(shop_country)
    shop_city = st.selectbox("City", s_cities, key="shop_city")
    shop_focus = st.text_input("What are you looking for?", placeholder="e.g. Clothes, Electronics, Local Crafts", key="shop_focus")

st.write('---')
shop_extra = st.text_area("Extra details (optional)", key="shop_extra")

if st.button("Find Shopping Places", key="shop_search"):
    if not shop_city or not shop_country:
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
            """
        prompt = f"""
            I am looking for shopping recommendations in {shop_city}, {shop_country}.
            I am specifically interested in {shop_type} and looking for {shop_focus}.
            Please provide {output_number} recommendations. For each place include:
            1. Name of the Place
            2. Type (Mall, Market, etc.)
            3. What they are best known for
            4. Approximate price range (Budget-friendly/Moderate/Expensive)
            5. Address
            6. Opening Hours if available
            Extra notes: {shop_extra}
            {pref_context}
            Please format the response clearly with each shopping place as a separate section.
            Make your answer short and focused only on what I requested.
            """
        with st.spinner('Finding the best places to shop...'):
            response = model.generate_content(prompt)
            st.write(response.text)
            pdf_content = generate_pdf_from_text(response.text)
            st.download_button(label='Download PDF ⬇️', data=pdf_content, file_name='shopping_recommendations.pdf', mime="application/pdf")

st.write('---')
st.caption('🌟 AI-powered recommendations using Google Gemini')
