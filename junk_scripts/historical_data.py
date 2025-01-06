import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_historical_weather(api_key, location, start_date, end_date):
    """
    Fetch historical weather data from WeatherAPI for a given date range.

    Args:
        api_key (str): WeatherAPI key.
        location (str): Location (city name, zip code, or lat/lon).
        start_date (str): Start date in the format YYYY-MM-DD.
        end_date (str): End date in the format YYYY-MM-DD.

    Returns:
        pd.DataFrame: DataFrame containing historical weather data.
    """
    url = "http://api.weatherapi.com/v1/history.json"
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    data_list = []

    for single_date in date_range:
        date_str = single_date.strftime('%Y-%m-%d')
        params = {
            "key": api_key,
            "q": location,
            "dt": date_str,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            day_data = data['forecast']['forecastday'][0]['day']
            data_list.append({
                "Date": date_str,
                "Max Temp (°C)": day_data['maxtemp_c'],
                "Min Temp (°C)": day_data['mintemp_c'],
                "Avg Temp (°C)": day_data['avgtemp_c'],
                "Precipitation (mm)": day_data['totalprecip_mm']
            })
        else:
            print(f"Failed to retrieve data for {date_str}: {response.text}")

    return pd.DataFrame(data_list)


def plot_weather_trends(weather_data):
    """
    Plot weather trends using Seaborn.

    Args:
        weather_data (pd.DataFrame): DataFrame containing weather data.
    """
    weather_data['Date'] = pd.to_datetime(weather_data['Date'])
    weather_data['Year'] = weather_data['Date'].dt.year
    weather_data['Month'] = weather_data['Date'].dt.month

    # Plot Average Temperature
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=weather_data, x='Date', y='Avg Temp (°C)', label='Avg Temp (°C)')
    plt.title('Average Temperature Over Time')
    plt.ylabel('Temperature (°C)')
    plt.xlabel('Date')
    plt.legend()
    plt.show()

    # Plot Max and Min Temperatures
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=weather_data, x='Date', y='Max Temp (°C)', label='Max Temp (°C)', color='red')
    sns.lineplot(data=weather_data, x='Date', y='Min Temp (°C)', label='Min Temp (°C)', color='blue')
    plt.title('Max and Min Temperatures Over Time')
    plt.ylabel('Temperature (°C)')
    plt.xlabel('Date')
    plt.legend()
    plt.show()

    # Plot Precipitation
    plt.figure(figsize=(12, 6))
    sns.barplot(data=weather_data, x='Month', y='Precipitation (mm)', hue='Year', ci=None)
    plt.title('Monthly Precipitation')
    plt.ylabel('Precipitation (mm)')
    plt.xlabel('Month')
    plt.legend(title='Year')
    plt.show()


# Example Usage
if __name__ == "__main__":
    api_key = 'a64189ecdf6d43a3b60164402250101'
    LOCATION = "New York"
    START_DATE = "2022-01-01"
    END_DATE = "2023-12-31"  # 2 years of data

    try:
        # Retrieve historical weather data
        weather_df = get_historical_weather(api_key, LOCATION, START_DATE, END_DATE)

        # Display the first few rows of the data
        print(weather_df.head())

        # Plot weather trends
        plot_weather_trends(weather_df)
    except Exception as e:
        print(f"Error: {e}")
