# Streamlit Program to Show a World Map and Retrieve City Names

# Install necessary libraries
# poetry addquit streamlit geopy
# Import libraries
import streamlit as st
from streamlit_folium import st_folium
import folium

from helper_functions import *

# Streamlit App
st.set_page_config(layout="wide")
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
        st.write(f"**City Name:** {city_name}")
        st.write(f"**Lat, Lon:** {lat:.3f}, {lon:.3f}")
        #st.write(f"**Longitude:** {lon:.3f}")
        #city_search.title(city_name)
        local_dt = get_local_time(lat, lon)
        st.write(f"**Local date time:** {local_dt}")

        weather_data = get_weather_data(city_name)

        print(type(weather_data))

        if "error" in weather_data:
            print(f"Error: {weather_data['error']}")
        else:
            # Extract and display relevant weather details
            print("\nWeather Details:")
            st.write(f"**City:** {weather_data['location']['name']}")
            st.write(f"**Region:** {weather_data['location']['region']}")
            st.write(f"**Country:** {weather_data['location']['country']}")
            st.write(f"**Temperature:** {weather_data['current']['temp_c']} °C")
            st.write(f"**Weather:** {weather_data['current']['condition']['text']}")
            st.write(f"**Humidity:** {weather_data['current']['humidity']}%")
            st.write(f"**Wind Speed:** {weather_data['current']['wind_kph']} kph")



# Add a second row with two columns
row2_col1, row2_col2 = st.columns([1, 1])

with row2_col1:
    st.write("## Weather Here")

with row2_col2:
    st.write("## Historical Weather Data")
    st.write("(Historical data integration coming soon!)")
