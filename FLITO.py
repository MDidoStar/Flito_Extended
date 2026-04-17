# Importing libraries
import streamlit as st
from datetime import date
from pymongo.mongo_client import MongoClient
from color import edit

st.set_page_config(page_title="FLITO: AI Travel Companion", page_icon='logo.png', layout="wide")

edit()


# --- Sidebar ---
with st.sidebar:
    st.logo(image='logo.png', size='large', icon_image='logo.png')
    
    
# --- MongoDB Setup (cached in session_state to prevent repeated connections) ---
if "mongo_ok" not in st.session_state:
    uri = st.secrets["mongodb_uri"]
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client["flito_db"]
        st.session_state["mongo_ok"] = True
        st.session_state["flito_db"] = db
        st.session_state["feedback_collection"] = db["feedback"]
    except Exception as e:
        st.session_state["mongo_ok"] = False
        st.session_state["mongo_error"] = str(e)

mongo_ok = st.session_state.get("mongo_ok", False)
feedback_collection = st.session_state.get("feedback_collection", None)
db = st.session_state.get("flito_db", None)

sme = st.session_state["mongo_error"]
if not sme == "":
    st.error(f"Error:{st.session_state["mongo_error"]}")




# --- Header ---
#st.markdown('<div class="hero-title">🌍 FLITO</div>', unsafe_allow_html=True)

import base64

# Load and encode the logo
with open("logo.png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

# --- Header ---
st.markdown(
    f'<div class="hero-title">'
    f'<img src="data:image/png;base64,{logo_b64}" style="height:50px; vertical-align:middle; margin-right:10px;">'
    f'FLITO'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="hero-subtitle">Your AI-powered travel companion — pick a tool and start exploring.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Greeting + Preferences ---
user = st.session_state.get("logged_in_user")
if user:
    first = user.get("first_name", user.get("Username", "Traveler"))
    last  = user.get("last_name", "")
    st.markdown(f'<div class="hero-subtitle">👋 Welcome back, <b>{first} {last}</b>! Great to have you here.</div>', unsafe_allow_html=True)

    with st.expander("⚙️ Your Travel Preferences", expanded=False):
        st.write("Tell us how you like to travel — these will personalize all AI suggestions.")
        existing_prefs = user.get("preferences", {})
        col1, col2 = st.columns(2)
        with col1:
            pref_language  = st.text_input("Preferred Language", value=existing_prefs.get("language", ""), key="pref_lang")
            budget_options = ["Budget-friendly", "Moderate", "Luxury"]
            budget_index = budget_options.index(existing_prefs.get("budget", "Moderate")) if existing_prefs.get("budget") in budget_options else 1
            pref_budget    = st.selectbox("Budget Style", budget_options, index=budget_index, key="pref_budget")
            food_options   = ["No preference", "Vegetarian", "Vegan", "Halal", "Seafood lover", "Local cuisine only"]
            food_index     = food_options.index(existing_prefs.get("food", "No preference")) if existing_prefs.get("food") in food_options else 0
            pref_food      = st.selectbox("Food Preference", food_options, index=food_index, key="pref_food")
        with col2:
            travel_options  = ["Explorer", "Relaxed", "Adventure", "Cultural", "Family", "Business"]
            travel_index    = travel_options.index(existing_prefs.get("travel_style", "Explorer")) if existing_prefs.get("travel_style") in travel_options else 0
            pref_travel     = st.selectbox("Travel Style", travel_options, index=travel_index, key="pref_travel")
            activity_options = ["Sightseeing", "Museums", "Beaches", "Shopping", "Nightlife", "Nature & Hiking"]
            activity_index   = activity_options.index(existing_prefs.get("activity", "Sightseeing")) if existing_prefs.get("activity") in activity_options else 0
            pref_activity   = st.selectbox("Favorite Activity", activity_options, index=activity_index, key="pref_activity")
            transport_options = ["Any", "Taxi", "Public Transport", "Car Rental", "Walking"]
            transport_index   = transport_options.index(existing_prefs.get("transport", "Any")) if existing_prefs.get("transport") in transport_options else 0
            pref_transport  = st.selectbox("Preferred Transport", transport_options, index=transport_index, key="pref_transport")

        if st.button("💾 Save Preferences", key="save_prefs"):
            new_prefs = {
                "language":     pref_language,
                "budget":       pref_budget,
                "food":         pref_food,
                "travel_style": pref_travel,
                "activity":     pref_activity,
                "transport":    pref_transport,
            }
            try:
                if db is not None:
                    db["users"].update_one(
                        {"Username": user["Username"]},
                        {"$set": {"preferences": new_prefs}}
                    )
                    st.session_state["logged_in_user"]["preferences"] = new_prefs
                    st.success("✅ Preferences saved! All AI tools will now use these.")
                else:
                    st.error("Database not available.")
            except Exception as e:
                st.error(f"Could not save preferences: {e}")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
else:
    st.info("Sign in or Sign Up to personalize your data")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown('<div class="section-label">Available Tools</div>', unsafe_allow_html=True)

# ------SignUp Card------#
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🔐 FLITO SignUp</div>
    <div class="app-card-desc">SignUp to make your preferences always with us</div>
</div>
""", unsafe_allow_html=True)
if st.button("Sign Up →", key="btn_signup"):
    st.switch_page("pages/Sign_In_or_Up.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Map ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🗺️ FLITO Map</div>
    <div class="app-card-desc">
        Explore destinations interactively. Search for any city, landmark, or address on a live map,
        detect your location, and click anywhere to get exact coordinates.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Map →", key="btn_map"):
    st.switch_page("pages/Map.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Hotels ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🏨 FLITO Hotels</div>
    <div class="app-card-desc">
        Find the best hotels tailored to your budget and star rating.
        Get detailed info including price per night, facilities, and contact details — powered by Gemini AI.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Hotels →", key="btn_hotels"):
    st.switch_page("pages/Hotels.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Food ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🍝 FLITO Food</div>
    <div class="app-card-desc">
        Discover top restaurants and cafes wherever you travel. Filter by cuisine, price,
        and rating to find your perfect dining experience.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Food →", key="btn_food"):
    st.switch_page("pages/Food.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Tourism ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🏝️ FLITO Tourism</div>
    <div class="app-card-desc">
        Discover museums, beaches, historical sites, and hidden gems.
        Filter by activity type and cost to plan the perfect day out.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Tourism →", key="btn_tourism"):
    st.switch_page("pages/Tourism.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Transportation ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🚗 FLITO Transportation</div>
    <div class="app-card-desc">
        Find the best way to get around — taxis, buses, trains, flights, or car rentals.
        Enter your origin and destination to get point-to-point recommendations.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Transportation →", key="btn_transport"):
    st.switch_page("pages/Transportation.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Shopping ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🛍️ FLITO Shopping</div>
    <div class="app-card-desc">
        Shop til you drop! Find malls, markets, boutiques, and outlet stores.
        Tell us what you're looking for and we'll find the best spots.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Shopping →", key="btn_shopping"):
    st.switch_page("pages/Shopping.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Budget ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">💰 FLITO Budget</div>
    <div class="app-card-desc">
        Track every expense of your trip in real-time. Set a total budget, log costs as you go,
        and always know exactly how much you have left.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Budget →", key="btn_budget"):
    st.switch_page("pages/Budget.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Currency ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">💱 FLITO Currency Converter</div>
    <div class="app-card-desc">
        Convert between any two currencies with live exchange rates.
        Supports hundreds of global currencies powered by ExchangeRate-API.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Currency →", key="btn_currency"):
    st.switch_page("pages/Currency.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Translation ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🗣️ FLITO Translation</div>
    <div class="app-card-desc">
        Translate text between 50+ languages instantly using Gemini AI.
        Get the meaning and pronunciation so you can communicate confidently anywhere.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Translation →", key="btn_translate"):
    st.switch_page("pages/Translation.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Card: Trip Builder ---
st.markdown("""
<div class="app-card">
    <div class="app-card-title">✈️ FLITO Trip Builder (Premium)</div>
    <div class="app-card-desc">
        The ultimate travel tool. Generate a complete day-by-day itinerary with hotels,
        restaurants, activities, and shopping — tailored to your dates, budget, and preferences.
        Supports voice input and PDF export. Premium access required.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Trip Builder →", key="btn_trip"):
    st.switch_page("pages/Trip_Builder.py")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Feedback Section ---
st.markdown('<div class="section-label">💬 Send Feedback</div>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])
with col1:
    st.write('Rate us (out of 5):')
    rating = st.feedback('stars', key="feedback_stars")
with col2:
    feedback_text = st.text_input("Any suggestions for improvement?", key="feedback_text_input")

if st.button('Send Feedback', key='send_feedback_btn'):
    if feedback_collection is not None:
        try:
            val_rating = rating + 1 if rating is not None else None
            feedback_data = {
                "rating": val_rating,
                "feedback": feedback_text,
                "date": str(date.today())
            }
            feedback_collection.insert_one(feedback_data)
            st.success("✅ Feedback saved! Thanks for your feedback 😊")
        except Exception as e:
            st.error(f"Failed to save feedback. Error: {e}")
    else:
        st.error("Database connection was not set up.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Admin Access ---
with st.expander("🔐 Admin Access"):
    admin_code = st.text_input("Enter admin code:", type="password", key="admin_code_input")
    ADMIN_CODE = st.secrets["Admin_code"]

    if st.button("📋 View All Feedbacks", key="view_feedbacks_btn"):
        if admin_code == ADMIN_CODE:
            if feedback_collection is not None:
                feedbacks = list(feedback_collection.find())
                if feedbacks:
                    for i, f in enumerate(feedbacks, 1):
                        st.markdown(f"**#{i}**")
                        st.write(f"⭐ Rating: {f.get('rating', 'N/A')}")
                        st.write(f"💬 Feedback: {f.get('feedback', 'N/A')}")
                        st.write(f"📅 Date: {f.get('date', 'N/A')}")
                        st.divider()
                else:
                    st.info("No feedbacks found.")
        else:
            st.error("❌ Wrong code.")

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    if st.button("🗑️ Clear All Feedbacks", key="clear_feedbacks_btn"):
        if admin_code == ADMIN_CODE:
            st.session_state.confirm_delete = True
        else:
            st.error("❌ Wrong code.")

    if st.session_state.confirm_delete:
        st.warning("⚠️ Are you sure? This will delete ALL feedbacks!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete All", key="yes_delete_btn"):
                if feedback_collection is not None:
                    result = feedback_collection.delete_many({})
                    st.success(f"Deleted {result.deleted_count} feedbacks.")
                st.session_state.confirm_delete = False
        with col2:
            if st.button("❌ Cancel", key="cancel_delete_btn"):
                st.session_state.confirm_delete = False

# --- Footer ---
st.caption('🌟 AI-powered recommendations using Google Gemini | Currency data from ExchangeRate-API')



#pg.run()




