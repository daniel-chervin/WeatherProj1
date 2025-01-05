import requests
import pandas as pd


def get_weather_forecast(api_key, location, days=3):
    """
    Fetch forecast weather data from WeatherAPI and organize it into a table.

    Args:
        api_key (str): WeatherAPI key.
        location (str): Location (city name, zip code, or lat/lon).
        days (int): Number of days to forecast (max 10).

    Returns:
        pd.DataFrame: DataFrame containing the forecast.
    """
    # WeatherAPI endpoint
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": location,
        "days": days,
    }

    # API request
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()

        # Extract relevant data
        forecast_days = data["forecast"]["forecastday"]
        forecast_list = []
        for day in forecast_days:
            date = day["date"]
            day_info = day["day"]
            forecast_list.append({
                "Date": date,
                "Max Temp (°C)": day_info["maxtemp_c"],
                "Min Temp (°C)": day_info["mintemp_c"],
                "Condition": day_info["condition"]["text"],
                "Rain Chance (%)": day_info.get("daily_chance_of_rain", "N/A"),
                "Snow Chance (%)": day_info.get("daily_chance_of_snow", "N/A"),
            })

        # Create DataFrame
        forecast_df = pd.DataFrame(forecast_list)
        return forecast_df
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


# Example usage
if __name__ == "__main__":
    api_key = 'a64189ecdf6d43a3b60164402250101'
    LOCATION = "New York"
    DAYS = 3

    try:
        # Fetch weather forecast
        forecast_df = get_weather_forecast(api_key, LOCATION, DAYS)

        # Display table
        print("Weather Forecast:")
        print(forecast_df.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")
