import hashlib
import google.generativeai as genai
import streamlit as st
import random
from datetime import date
from pymongo.mongo_client import MongoClient
from color import edit

st.set_page_config(page_title="FLITO: Sign Up", page_icon='logo.png', layout="wide")
edit()

genai.configure(api_key=st.secrets["gemini_api_key"])
model = genai.GenerativeModel('gemini-2.5-flash')

st.markdown('<div class="hero-title">🔐 FLITO Sign In or Sign Up</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Create your account to start exploring.</div>', unsafe_allow_html=True)
st.markdown("---")
with st.expander("🔐 Sign Up"):
    st.subheader("Enter Your Data For Flito 🌍")
    
    first_name = st.text_input("First Name", key="fm")
    last_name  = st.text_input("Last Name",  key="lm")
    Username   = st.text_input("Username",   key="user")
    p          = st.text_input(
        "Password — Flito does not show your password for safety reasons, please keep it safe.",
        key="pass", type="password"
    )
    age   = st.number_input("Age", min_value=8, max_value=100, key="age")
    Email = st.text_input("Email", key="nmail")
    Phone = st.text_input("Enter Phone Number (Optional)")
    
    button1 = st.button("Enter all data")
    prompt = f''' Answer the following with Either 1 or 0 only 1 means yes 0 means no check if this email:"{Email} is valid'''
    if button1:
        response = model.generate_content(prompt)

        # --- Validation ---
        if not first_name:
            st.error("Please enter your First Name.")
        elif not last_name:
            st.error("Please enter your Last Name.")
        elif not Username:
            st.error("Please enter a Username.")
        elif not p:
            st.error("Please enter a Password.")
        elif not Email or response.text == 0:
            st.error("Please enter a valid Email.")
        else:
            # All fields valid — show summary and mark as confirmed
            phone_display = Phone if Phone else "Not provided"
            first_nam = first_name.capitalize()
            last_nam  = last_name.capitalize()
    
            st.success(f"""
            Dear {first_nam} {last_nam}, here are your Flito credentials:
            \n**Name:** {first_nam} {last_nam}
            \n**Age:** {age} years old
            \n**Username:** {Username}
            \n**Email:** {Email}
            \n**Phone (Optional):** {phone_display}
            \n**Password:** {len(p)} characters long (hidden for safety)
            """)
    
            # Store data in session_state so it survives the next render
            st.session_state["signup_data"] = {
                "first_name": first_nam,
                "last_name":  last_nam,
                "Username":   Username,
                "Email":      Email,
                "password":   hashlib.sha256(p.encode()).hexdigest(),
                "Phone":      phone_display,
                "age":        age,
                "date":       str(date.today()),
                "preferences": {},  # filled later in FLITO.py
            }
    
    # --- "Go To Flito" appears only after data has been confirmed ---
    if "signup_data" in st.session_state:
        if st.button("Go To Flito"):
            uri = st.secrets["mongodb_uri"]
            try:
                client = MongoClient(uri, serverSelectionTimeoutMS=5000)
                client.admin.command("ping")
                db = client["flito_db"]
                users_collection = db["users"]
                mongo_ok = True
            except Exception as e:
                mongo_ok = False
                mongo_error = str(e)
    
            if not mongo_ok:
                st.error(f"❌ Connection failed: {mongo_error}")
                st.stop()
    
            st.success("✅ Connected to Flito database.")
    
            try:
                users_collection.insert_one(st.session_state["signup_data"])
                st.success("✅ Account created successfully! Thanks for joining Flito 😊")
                # Set logged_in_user so FLITO.py can greet them and show preferences
                st.session_state["logged_in_user"] = {
                    "Username":    st.session_state["signup_data"]["Username"],
                    "first_name":  st.session_state["signup_data"]["first_name"],
                    "last_name":   st.session_state["signup_data"]["last_name"],
                    "Email":       st.session_state["signup_data"]["Email"],
                    "Phone":       st.session_state["signup_data"]["Phone"],
                    "age":         st.session_state["signup_data"]["age"],
                    "date":        st.session_state["signup_data"]["date"],
                    "preferences": {},
                }
                del st.session_state["signup_data"]  # Clean up after saving
            except Exception as e:
                st.error(f"Failed to save your data. Error: {e}")
                st.stop()
    
            # Use a relative path — never hardcode an absolute local path
            st.switch_page("FLITO.py")

# ─────────────────────────────────────────────
# Admin panel (always visible to admins, but separate from the signup flow)
# ─────────────────────────────────────────────
with st.expander("🔐 Admin Access"):
    admin_code  = st.text_input("Enter admin code:", type="password", key="admin_code")
    ADMIN_CODE  = st.secrets.get("Admin_code")

    uri = st.secrets["mongodb_uri"]
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client["flito_db"]
        users_collection = db["users"]
        mongo_ok = True
    except Exception:
        mongo_ok = False

    if st.button("📋 View All Users", key="btn_all_users"):
        if admin_code == ADMIN_CODE and mongo_ok:
            users = list(users_collection.find())
            if users:
                for i, u in enumerate(users, 1):
                    st.markdown(f"**#{i}**")
                    st.write(f"👤 Username:   {u.get('Username',   'N/A')}")
                    st.write(f"🧑 Name:       {u.get('first_name', 'N/A')} {u.get('last_name', '')}")
                    st.write(f"📧 Email:      {u.get('Email',      'N/A')}")
                    st.write(f"🎂 Age:        {u.get('age',        'N/A')}")
                    st.write(f"📅 Date:       {u.get('date',       'N/A')}")
                    prefs = u.get("preferences", {})
                    if prefs:
                        st.write("⚙️ **Preferences:**")
                        for k, v in prefs.items():
                            st.write(f"  • {k.replace('_', ' ').capitalize()}: {v}")
                    else:
                        st.write("⚙️ Preferences: Not set yet")
                    st.divider()
            else:
                st.info("No users found.")
        else:
            st.error("❌ Wrong code or database unavailable.")

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    if st.button("🗑️ Clear All Users", key="btn_clear"):
        if admin_code == ADMIN_CODE:
            st.session_state.confirm_delete = True
        else:
            st.error("❌ Wrong code.")

    if st.session_state.confirm_delete:
        st.warning("⚠️ Are you sure? This will delete ALL user records!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete All", key="btn_yes_delete"):
                result = users_collection.delete_many({})
                st.success(f"Deleted {result.deleted_count} user(s).")
                st.session_state.confirm_delete = False
        with col2:
            if st.button("❌ Cancel", key="btn_cancel_delete"):
                st.session_state.confirm_delete = False


    #Sign In
with st.expander("🔐 Sign In"):
    email_username = st.text_input("Enter your Email/Username:", key="emaiuserl")
    pass_sign_in   = st.text_input("Enter your Password:", type="password", key="admin_coe")

    uri = st.secrets["mongodb_uri"]
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client["flito_db"]
        users_collection = db["users"]
        mongo_ok = True
    except Exception:
        mongo_ok = False

    if st.button("📋 Sign In", key="btn_all_uses"):
        if not email_username or not pass_sign_in:
            st.error("Please enter both your Email/Username and Password.")
        elif not mongo_ok:
            st.error("❌ Database unavailable.")
        else:
            # Hash the entered password to compare with stored hash
            hashed_input = hashlib.sha256(pass_sign_in.encode()).hexdigest()

            # Search by Username OR Email
            user = users_collection.find_one({
                "$or": [
                    {"Username": email_username},
                    {"Email":    email_username}
                ]
            })

            if user is None:
                st.error("❌ No account found with that username or email.")
            elif user.get("password") != hashed_input:
                st.error("❌ Incorrect password.")
            else:
                st.success(f"✅ Welcome back, {user.get('first_name', '')} {user.get('last_name', '')}! 👋")
                st.session_state["logged_in_user"] = {
                    "Username":   user.get("Username"),
                    "first_name": user.get("first_name"),
                    "last_name":  user.get("last_name"),
                    "Email":      user.get("Email"),
                    "Phone":      user.get("Phone"),
                    "age":        user.get("age"),
                    "date":       user.get("date"),
                    "preferences": user.get("preferences", {}),
                }
                st.switch_page("FLITO.py")
                    
