# https://www.weatherapi.com/    weather api key: a64189ecdf6d43a3b60164402250101

# Import libraries
import requests
import json

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

# Main block for user interaction
print("Welcome to the Weather Fetching Application!")
api_key =  'a64189ecdf6d43a3b60164402250101' # input("Enter your WeatherAPI key: ")
city_name = 'Jerusalem' #input("Enter the name of the city: ")

# Fetch weather data
weather_data = get_weather_data(city_name, api_key)

print(type(weather_data))

if "error" in weather_data:
    print(f"Error: {weather_data['error']}")
else:
    # Extract and display relevant weather details
    print("\nWeather Details:")
    print(f"City: {weather_data['location']['name']}")
    print(f"Region: {weather_data['location']['region']}")
    print(f"Country: {weather_data['location']['country']}")
    print(f"Temperature: {weather_data['current']['temp_c']} °C")
    print(f"Weather: {weather_data['current']['condition']['text']}")
    print(f"Humidity: {weather_data['current']['humidity']}%")
    print(f"Wind Speed: {weather_data['current']['wind_kph']} kph")