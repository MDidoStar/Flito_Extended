# Importing libraries
import streamlit as st
from datetime import date
from pymongo.mongo_client import MongoClient
from color import edit



st.set_page_config(page_title="FLITO: AI Traveling Blogger", page_icon='logo.png', layout="wide")

edit()

# --- Single MongoDB Setup (flito_db) ---
uri = st.secrets["mongodb_uri"]
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    db = client["flito_db"]
    feedback_collection = db["feedback"]
    mongo_ok = True
except Exception as e:
    feedback_collection = None
    mongo_ok = False
    mongo_error = str(e)

# --- Sidebar ---
with st.sidebar:
    st.logo(image='logo.png', size='large', icon_image='logo.png')

    # Connection status
    if mongo_ok:
        st.success("✅ Connected to flito")
    else:
        st.error(f"❌ Connection failed: {mongo_error}")
        st.stop()

    st.header("Customize the app!")
    output_number = st.slider("How many outputs shall I suggest?:", 1, 10, 1, key="output_num")
    st.divider()

    # --- Feedback Section ---
    st.subheader("💬 Send Feedback")
    st.write('Rate us (out of 5):')
    rating = st.feedback('stars', key="trip_rating")
    feedback = st.text_input("Any suggestions for improvement?")
    if st.button('Send Feedback', key='feedback_btn'):
        if feedback_collection is not None:
            try:
                val_rating = rating + 1 if rating is not None else None
                feedback_data = {
                    "rating": val_rating,
                    "feedback": feedback,
                    "date": str(date.today())
                }
                feedback_collection.insert_one(feedback_data)
                st.success("✅ Feedback saved to Flito, Thanks For your feedback 😊!")
            except Exception as e:
                st.error(f"Failed to save feedback. Error: {e}")
        else:
            st.error("Database connection was not set up.")

    st.divider()

    # --- Admin Access ---
    st.subheader("🔐 Admin Access")
    admin_code = st.text_input("Enter admin code:", type="password", key="admin_code")
    ADMIN_CODE = st.secrets["Admin_code"]

    if st.button("📋 All Feedbacks", key="btn_all_feedbacks"):
        if admin_code == ADMIN_CODE:
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

    if st.button("🗑️ Clear All Feedbacks", key="btn_clear"):
        if admin_code == ADMIN_CODE:
            st.session_state.confirm_delete = True
        else:
            st.error("❌ Wrong code.")

    if st.session_state.confirm_delete:
        st.warning("⚠️ Are you sure? This will delete ALL feedbacks!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete All", key="btn_yes_delete"):
                result = feedback_collection.delete_many({})
                st.success(f"Deleted {result.deleted_count} feedbacks.")
                st.session_state.confirm_delete = False
        with col2:
            if st.button("❌ Cancel", key="btn_cancel_delete"):
                st.session_state.confirm_delete = False

   # st.subheader('Would you like to go Premium?')
   # st.link_button('Subscribe now!', 'https://buy.stripe.com/test_3cIcN592b5iLfN93mU8so00')

# --- Header ---
st.markdown('<div class="hero-title">🌍 FLITO</div>', unsafe_allow_html=True)
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
        col1, col2 = st.columns(2)
        with col1:
            pref_language   = st.text_input("Preferred Language",key="pref_lang")
            pref_budget     = st.selectbox("Budget Style",          ["Budget-friendly", "Moderate", "Luxury"], index=1, key="pref_budget")
            pref_food       = st.selectbox("Food Preference",       ["No preference", "Vegetarian", "Vegan", "Halal", "Seafood lover", "Local cuisine only"], key="pref_food")
        with col2:
            pref_travel     = st.selectbox("Travel Style",          ["Explorer", "Relaxed", "Adventure", "Cultural", "Family", "Business"], key="pref_travel")
            pref_activity   = st.selectbox("Favorite Activity",     ["Sightseeing", "Museums", "Beaches", "Shopping", "Nightlife", "Nature & Hiking"], key="pref_activity")
            pref_transport  = st.selectbox("Preferred Transport",   ["Any", "Taxi", "Public Transport", "Car Rental", "Walking"], key="pref_transport")

        if st.button("💾 Save Preferences", key="save_prefs"):
            new_prefs = {
                "language":   pref_language,
                "budget":     pref_budget,
                "food":       pref_food,
                "travel_style": pref_travel,
                "activity":   pref_activity,
                "transport":  pref_transport,
            }
            try:
                db["users"].update_one(
                    {"Username": user["Username"]},
                    {"$set": {"preferences": new_prefs}}
                )
                st.session_state["logged_in_user"]["preferences"] = new_prefs
                st.success("✅ Preferences saved! All AI tools will now use these.")
            except Exception as e:
                st.error(f"Could not save preferences: {e}")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
else:
    st.info("Sign in or Up to personalize your data")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown('<div class="section-label">Available Tools</div>', unsafe_allow_html=True)


#-----Navigation--------#
pg = st.navigation([
    st.Page("pages/sign_up.py", title="Sign In or Up", icon="🔐"),
    st.Page("pages/Map.py", title="Map", icon="🗺️"),
    st.Page("pages/Hotels.py", title="Hotels", icon="🏨"),
    st.Page("pages/Food.py", title="Food", icon="🍝"),
    st.Page("pages/Tourism.py", title="Tourism", icon="🏝️"),
    st.Page("pages/Transportation.py", title="Transportation", icon="🚗"),
    st.Page("pages/Shopping.py", title="Shopping", icon="🛍️"),
    st.Page("pages/Budget.py", title="Budget", icon="💰"),
    st.Page("pages/Currency.py", title="Currency Converter", icon="💱"),
    st.Page("pages/Translation.py", title="Translation", icon="🗣️"),
    st.Page("pages/Trip_Builder.py", title="Trip Builder", icon="✈️")
])

pg.run()  # ✅ called once, on the object returned by st.navigation()


# ------SignUp Card------#
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🔐 FLITO SignUp</div>
    <div class="app-card-desc">
        SignUp to make your prefrences always with us
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Sign Up →", key="btn_sihnup"):
    st.switch_page("pages/sign_up.py")
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
    <div class="app-card-title">🏨FLITO Hotels</div>
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
    <div class="app-card-title">🍝FLITO Food</div>
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
    <div class="app-card-title">🏝️FLITO Tourism</div>
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
    <div class="app-card-title">🚗FLITO Transportation</div>
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
    <div class="app-card-title">🛍️FLITO Shopping</div>
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
    <div class="app-card-title">💰FLITO Budget</div>
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
    <div class="app-card-title">💱FLITO Currency Converter</div>
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
    <div class="app-card-title">🗣️FLITO Translation</div>
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
    <div class="app-card-title">✈️FLITO Trip Builder (Premium)</div>
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




# --- Footer ---
st.caption('🌟 AI-powered recommendations using Google Gemini | Currency data from ExchangeRate-API')
