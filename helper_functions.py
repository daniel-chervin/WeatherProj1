#on virtual env: "pip install" or "poetry add" streamlit geopy pytz

import requests
from datetime import datetime
import pytz

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

import json

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

# Function to fetch weather data from WeatherAPI
def get_weather_data(city_name, api_key):
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
    api_key = 'a64189ecdf6d43a3b60164402250101'  # input("Enter your WeatherAPI key: ")

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