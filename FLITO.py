# Importing libraries
import streamlit as st
from datetime import date
from pymongo.mongo_client import MongoClient
from color import edit

st.set_page_config(page_title="FLITO: AI Traveling Blogger", page_icon='logo.png', layout="wide")

edit()

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

# --- Sidebar ---
with st.sidebar:
    st.logo(image='logo.png', size='large', icon_image='logo.png')

    # --- Navigation ---
    pg = st.navigation([
        st.Page("pages/home.py", title="Main Page (FLITO)", icon="🌍"),
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
        st.Page("pages/Trip_Builder.py", title="Trip Builder", icon="✈️"),
    ])
    st.switch_page("pages/home.py")

# --- Run the selected page ---
# pg.run() hands off rendering to whichever page is active.
# st.stop() then halts FLITO.py so the main page content below
# does NOT render on top of other pages.
pg.run()


# ─────────────────────────────────────────────────────────────────────────────
# Everything below only executes when FLITO.py itself is the active page.
# st.stop() above exits early for all other pages before reaching this point.
# ─────────────────────────────────────────────────────────────────────────────
