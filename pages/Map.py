
# Importing libraries
import folium
import streamlit as st
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
from folium.plugins import LocateControl
from color import edit
st.set_page_config(page_title="FLITO: Map", page_icon='logo.png', layout="wide")

edit()

st.title("🌍 FLITO 🗺️ Map")

show_location = st.toggle("Show your location")


with st.sidebar:
    st.logo(image='logo.png', size='large', icon_image='logo.png')
    st.divider()
    if st.button("← Back to FLITO", key="back_btn"):
        st.switch_page("E:\Coding Mohamed\Flito Extened\Flito-main\FLITO.py")



# --- Map Tab ---

if show_location:
    st.write("Check our interactive map...")
        
    col1, col2 = st.columns([3, 1]) 
    with col1:
        search_query = st.text_input("🔍 Search for a location", placeholder="Enter city, address, or landmark...", label_visibility="collapsed")
        
    default_lat, default_lon = 30.0444, 31.2357
    map_center = [default_lat, default_lon]
    zoom_level = 12
        
    if search_query:
        try:
            # FIX: Added 'timeout=10' to wait up to 10 seconds for a response
            geolocator = Nominatim(user_agent="streamlit_map_app", timeout=10)
                
            with st.spinner(f"Searching for '{search_query}'..."):
                location = geolocator.geocode(search_query)
                
            if location:
                map_center = [location.latitude, location.longitude]
                zoom_level = 15
                st.success(f"📍 Found: {location.address}")
            else:
                    st.warning(f"Location '{search_query}' not found. Showing default location.")
        except Exception as e:
            st.error(f"Error searching location: {str(e)}")

    m = folium.Map(location=map_center, zoom_start=zoom_level)
        
    if search_query and 'location' in locals() and location:
        folium.Marker(
            [location.latitude, location.longitude], 
            popup=location.address, 
            tooltip="Searched Location", 
            icon=folium.Icon(color='red', icon='search')
        ).add_to(m)
        
    LocateControl(auto_start=False).add_to(m)
        
    output = st_folium(m, height=700, use_container_width=True, returned_objects=["last_clicked"])
        
    if output["last_clicked"]:
        st.success(f"Your Location Selected:\nLatitude: {output['last_clicked']['lat']:.5f}, Longitude: {output['last_clicked']['lng']:.5f}")
    else:
        st.info("Click on the map or use the location button to specify your current location.")
else:
    st.info("Select 'Show Location' in the sidebar to view your real-time location on the map.")


