import requests
api_key = 'a64189ecdf6d43a3b60164402250101'  # input("Enter your WeatherAPI key: ")

def get_historical_weather(city_name, date):
    """
    Retrieve historical weather data from WeatherAPI.

    Parameters:
        api_key (str): Your WeatherAPI key.
        city_name (str): Name of the city.
        date (str): Date in 'YYYY-MM-DD' format.

    Returns:
        dict: Weather data including temperature and precipitation.
    """
    url = f"http://api.weatherapi.com/v1/history.json"
    params = {
        "key": api_key,
        "q": city_name,
        "dt": date
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "forecast" in data:
                forecast = data["forecast"]["forecastday"][0]["day"]
                return {
                    "date": date,
                    "avg_temp_c": forecast.get("avgtemp_c", None),
                    "total_precip_mm": forecast.get("totalprecip_mm", None)
                }
            else:
                return {"error": "No forecast data available."}
        else:
            return {"error": f"HTTP error {response.status_code}: {response.reason}, "}
    except requests.RequestException as e:
        return {"error": str(e)}

# Example usage
city_name = "New York"
date = "2022-01-01"

weather_data = get_historical_weather(city_name, date)
if "error" in weather_data:
    print(f"Error: {weather_data['error']}")
else:
    print(f"Weather on {weather_data['date']} in {city_name}:")
    print(f"  Average Temperature: {weather_data['avg_temp_c']} °C")
    print(f"  Total Precipitation: {weather_data['total_precip_mm']} mm")
