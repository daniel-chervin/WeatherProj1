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
    geolocator = Nominatim(user_agent="danielc_locator")
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, language="en", timeout=15)
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
    geolocator = Nominatim(user_agent="danielc_locator")
    try:
        location = geolocator.geocode(city_name, exactly_one=True, language="en", timeout=15)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return None
    return None

# Function to fetch weather data from WeatherAPI
def get_weather_data(location, query_type="current", days=1, start_date=None):
    """
    Query weather data from WeatherAPI.

    Args:
        location (str): Location to query (e.g., city name, zip code, or lat/lon).
        query_type (str): Type of query ('current', 'forecast', 'history').
        days (int): Number of days for forecast (only used if query_type is 'forecast').
        start_date (str): Start date for historical data in 'YYYY-MM-DD' format (only used if query_type is 'history').

    Returns:
        dict: Weather data as a Python dictionary.
    """
    # Base URL
    base_url = "http://api.weatherapi.com/v1"

    # Endpoint selection
    if query_type == "current":
        endpoint = f"{base_url}/current.json"
        params = {"key": api_key, "q": location}
    elif query_type == "forecast":
        endpoint = f"{base_url}/forecast.json"
        params = {"key": api_key, "q": location, "days": days}
    elif query_type == "history":
        if not start_date:
            raise ValueError("start_date is required for historical queries.")
        endpoint = f"{base_url}/history.json"
        params = {"key": api_key, "q": location, "dt": start_date}
    else:
        raise ValueError("Invalid query_type. Use 'current', 'forecast', or 'history'.")

    # Make the API request

    try:
        response = requests.get(endpoint, params=params, timeout=15)  # Timeout is set to 10 seconds
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        #print(response.text)
    except requests.exceptions.Timeout:
        raise Exception(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error {response.status_code}: {response.text}")

    # Check for a successful response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

