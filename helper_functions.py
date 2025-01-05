#on virtual env: "pip install" or "poetry add" streamlit geopy pytz streamlit_folium seaborn

import requests
import streamlit as st
import seaborn as sns
from datetime import datetime
import pytz

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

import json
import pandas as pd
from matplotlib import pyplot as plt
from timezonefinder import TimezoneFinder

api_key = 'a64189ecdf6d43a3b60164402250101'  # input("Enter your WeatherAPI key: ")


def get_local_datetime(lat, lon):
    """
    Retrieve the local date and time for given latitude and longitude using TimezoneFinder.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        str: Local date and time at the given location.
    """
    # Initialize TimezoneFinder
    tf = TimezoneFinder()

    # Get the timezone string from latitude and longitude
    timezone_str = tf.timezone_at(lat=lat, lng=lon)

    if timezone_str:
        # Get the current local time in the timezone
        tz = pytz.timezone(timezone_str)
        local_time = datetime.now(tz)
        return local_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return "Timezone not found for the given coordinates."

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

# Function to fetch weather data from WeatherAPI
def get_weather_data(city_name):

    """
    Fetch weather data for a specified city.

    Parameters:
        city_name (str): Name of the city to fetch weather for.
        api_key (str): API key for WeatherAPI.

    Returns:
        dict: Parsed JSON data containing weather information, or error details.
    """
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": city_name,
        "aqi": "yes"  # include air quality data
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("error", {}).get("message", "Unable to fetch weather data.")}

def get_historical_weather(city_name, years):
    """
    Get historical weather data for a city over a range of years.

    Parameters:
        api_key (str): API key for WeatherAPI.
        city_name (str): Name of the city.
        years (list): List of years to retrieve data for.

    Returns:
        list: List of dictionaries containing year, temperature, and precipitation.
    """
    base_url = "http://api.weatherapi.com/v1/history.json"
    data = []
    for year in years:
        date = f"{year}-01-01"
        params = {
            "key": api_key,
            "q": city_name,
            "dt": date
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            if "forecast" in weather_data:
                forecast = weather_data["forecast"]["forecastday"][0]
                temp = forecast["day"]["avgtemp_c"]
                precip = forecast["day"]["totalprecip_mm"]
                data.append({"year": year, "temperature": temp, "precipitation": precip})
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