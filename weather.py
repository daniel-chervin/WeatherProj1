import requests

def get_weather_data(api_key, location, query_type="current", days=1, start_date=None):
    """
    Query weather data from WeatherAPI.

    Args:
        api_key (str): Your WeatherAPI key.
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
    response = requests.get(endpoint, params=params)

    # Check for a successful response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Example usage
if __name__ == "__main__":
    # Replace with your WeatherAPI key
    api_key = 'a64189ecdf6d43a3b60164402250101'  # input("Enter your WeatherAPI key: ")


    # Location to query (e.g., city name, zip code, or lat/lon)
    location = "London"

    # Query for current weather
    try:
        weather_data = get_weather_data(api_key, location, query_type="current")
        #weather_data = get_weather(api_key, "New York", query_type="forecast", days=3)
        #weather_data = get_weather(api_key, "Tokyo", query_type="history", start_date="2023-12-25")

        print("Current Weather Data:")
        print(weather_data)
    except Exception as e:
        print(f"Error: {e}")
