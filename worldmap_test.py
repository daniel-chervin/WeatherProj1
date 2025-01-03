# Streamlit Program to Show a World Map and Retrieve City Names

# Install necessary libraries
# poetry addquit streamlit geopy

# Import libraries
import streamlit as st
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Initialize Geolocator
def get_city_from_coords(lat, lon):
    """
    Get the city name from latitude and longitude coordinates.

    Parameters:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        str: Name of the city in English or a message if not found.
    """
    geolocator = Nominatim(user_agent="city_locator")
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, language="en")
        if location and "address" in location.raw:
            address = location.raw["address"]
            return address.get("city", "Unknown city")
    except GeocoderTimedOut:
        return "Geocoding timed out. Please try again."
    return "City not found"

# Streamlit App
st.title("Interactive World Map to Retrieve City Names")
st.write("Click on the map to retrieve the city name for the selected location.")

# Create a Folium map
map_center = [0, 0]  # Center of the map (latitude, longitude)
zoom_start = 2  # Default zoom level
m = folium.Map(location=map_center, zoom_start=zoom_start)

# Add map to Streamlit
map_data = st_folium(m, width=700, height=500)

# Handle map click event
if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
    last_clicked = map_data["last_clicked"]
    lat = last_clicked["lat"]
    lon = last_clicked["lng"]
    city_name = get_city_from_coords(lat, lon)
    st.write(f"Selected Location: Latitude = {lat}, Longitude = {lon}")
    st.write(f"City Name: {city_name}")

