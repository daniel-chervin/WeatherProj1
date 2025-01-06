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

def get_coords_from_city(city_name):
    """
    Get latitude and longitude coordinates from a city name.

    Parameters:
        city_name (str): Name of the city.

    Returns:
        tuple: Latitude and longitude of the city or None if not found.
    """
    geolocator = Nominatim(user_agent="city_locator")
    try:
        location = geolocator.geocode(city_name, exactly_one=True, language="en")
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return None
    return None

# Streamlit App
st.title("Interactive World Map to Retrieve City Names")
st.write("Click on the map to retrieve the city name for the selected location, or search for a city to focus on it.")

# Layout with 1 row and 2 columns
col1, col2 = st.columns([2, 1])

# Create a Folium map in the left column
with col1:
    map_center = [0, 0]  # Default center of the map (latitude, longitude)
    zoom_start = 2  # Default zoom level

    # City search input
    city_search = st.text_input("Search for a city:")
    if city_search:
        coords = get_coords_from_city(city_search)
        if coords:
            map_center = [coords[0], coords[1]]
            zoom_start = 12
        else:
            st.write("City not found. Please try another city.")

    # Initialize map with updated center
    m = folium.Map(location=map_center, zoom_start=zoom_start)

    # Add marker if city is found
    if city_search and coords:
        folium.Marker(location=coords, popup=city_search).add_to(m)

    # Add Folium map to Streamlit
    map_data = st_folium(m, width=700, height=500)

# Display selected location and city name in the right column
with col2:
    st.write("### Selected Location and City")
    if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
        last_clicked = map_data["last_clicked"]
        lat = last_clicked["lat"]
        lon = last_clicked["lng"]
        city_name = get_city_from_coords(lat, lon)
        st.write(f"**Latitude:** {lat}")
        st.write(f"**Longitude:** {lon}")
        st.write(f"**City Name:** {city_name}")
        #city_search.title(city_name)

    # Display city details from search

    #if city_search and coords:
    #    st.write("### City Details from Search")
    #    st.write(f"**City Name:** {city_search}")
    #    st.write(f"**Latitude:** {coords[0]}")
    #    st.write(f"**Longitude:** {coords[1]}")
