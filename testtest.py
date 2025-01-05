# Streamlit Program to Show a World Map and Retrieve City Names

# Install necessary libraries


# Import libraries
import streamlit as st
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import datetime
import pytz
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

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

def get_local_time(lat, lon):
    """
    Get the local time for a given latitude and longitude.

    Parameters:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        str: Local time in the format YYYY-MM-DD HH:MM:SS.
    """
    try:
        timezone = pytz.timezone(pytz.country_timezones(pytz.country_names["United States"])[0])  # Default to UTC if timezone cannot be determined
        local_time = datetime.now(timezone)
        return local_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return "Time not available"

def get_historical_weather(api_key, city_name, years):
    """
    Get historical weather data for a city over a range of years.

    Parameters:
        api_key (str): API key for Open-Meteo API.
        city_name (str): Name of the city.
        years (list): List of years to retrieve data for.

    Returns:
        list: List of dictionaries containing year, temperature, and precipitation.
    """
    coords = get_coords_from_city(city_name)
    if not coords:
        return []

    lat, lon = coords
    data = []
    for year in years:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        url = f"https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ["temperature_2m_max", "precipitation_sum"],
            "timezone": "auto"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            if "daily" in weather_data:
                daily_data = weather_data["daily"]
                avg_temp = sum(daily_data["temperature_2m_max"])/len(daily_data["temperature_2m_max"])
                total_precip = sum(daily_data["precipitation_sum"])
                data.append({"year": year, "temperature": avg_temp, "precipitation": total_precip})
    return data

def plot_weather_data(data):
    """
    Plot weather data using seaborn.

    Parameters:
        data (list): List of dictionaries containing year, temperature, and precipitation.

    Displays:
        A seaborn graph showing temperature and precipitation over years.
    """
    df = pd.DataFrame(data)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    sns.lineplot(data=df, x="year", y="temperature", ax=ax1, label="Temperature (°C)", color="blue")
    ax1.set_ylabel("Temperature (°C)", color="blue")
    ax2 = ax1.twinx()
    sns.lineplot(data=df, x="year", y="precipitation", ax=ax2, label="Precipitation (mm)", color="green")
    ax2.set_ylabel("Precipitation (mm)", color="green")

    ax1.set_title("Historical Weather Data")
    ax1.set_xlabel("Year")

    st.pyplot(fig)

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
        local_time = get_local_time(lat, lon)
        st.write(f"**Latitude:** {lat}")
        st.write(f"**Longitude:** {lon}")
        st.write(f"**City Name:** {city_name}")
        st.write(f"**Local Time:** {local_time}")

    # Display city details from search
    if city_search and coords:
        st.write("### City Details from Search")
        st.write(f"**City Name:** {city_search}")
        st.write(f"**Latitude:** {coords[0]}")
        st.write(f"**Longitude:** {coords[1]}")
        local_time = get_local_time(coords[0], coords[1])
        st.write(f"**Local Time:** {local_time}")

# Add a second row with two columns
row2_col1, row2_col2 = st.columns([1, 1])

with row2_col1:
    st.write("## Weather Here")

with row2_col2:
    st.write("## Historical Weather Data")
    years = st.multiselect("Select years to view:", options=list(range(2000, 2024)), default=[2020, 2021])
    if city_search and years:
        historical_data = get_historical_weather("", city_search, years)
        if historical_data:
            plot_weather_data(historical_data)
        else:
            st.write("No historical data available.")
