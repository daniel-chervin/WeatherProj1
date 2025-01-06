import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# API Key and Base URL
API_KEY = 'a64189ecdf6d43a3b60164402250101'  # input("Enter your WeatherAPI key: ")

BASE_URL = "http://api.weatherapi.com/v1/history.json"


# Function to fetch data from WeatherAPI
#@st.cache
def fetch_weather_data(location, start_date, end_date):
    all_data = []
    current_date = pd.to_datetime(start_date)
    while current_date <= pd.to_datetime(end_date):
        params = {
            "key": API_KEY,
            "q": location,
            "dt": current_date.strftime("%Y-%m-%d")
        }
        print(params)
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            day_data = response.json()["forecast"]["forecastday"][0]["hour"]
            all_data.extend(day_data)
        else:
            st.error(f"Error fetching data: {response.status_code}")
            break
        current_date += pd.Timedelta(days=1)

    return pd.DataFrame(all_data)


# Streamlit UI for user input
st.title("WeatherAPI Data Visualizations")
location = st.text_input("Enter location:", value="London")
start_date = st.date_input("Start Date:", value=pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date:", value=pd.to_datetime("2023-01-07"))

if st.button("Fetch Weather Data"):
    # Fetch the data
    data = fetch_weather_data(location, start_date, end_date)
    st.success("Data fetched successfully!")
    data

    # Process data for visualization
    data["time"] = pd.to_datetime(data["time"])
    data["date"] = data["time"].dt.date
    data["hour"] = data["time"].dt.hour

    st.dataframe(data.head())

    # Visualization 1: Temperature Trend
    st.subheader("Temperature Trend")
    fig, ax = plt.subplots()
    sns.lineplot(data=data, x="time", y="temp_c", ax=ax, label="Temperature (°C)")
    ax.set_title("Hourly Temperature Trend")
    st.pyplot(fig)

    # Visualization 2: Humidity vs. Temperature
    st.subheader("Humidity vs. Temperature")
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x="temp_c", y="humidity", ax=ax)
    ax.set_title("Humidity vs. Temperature")
    st.pyplot(fig)

    # Visualization 3: Precipitation Analysis
    st.subheader("Precipitation Analysis")
    daily_precip = data.groupby("date")["precip_mm"].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=daily_precip, x="date", y="precip_mm", ax=ax)
    ax.set_title("Daily Precipitation")
    st.pyplot(fig)

    # Visualization 4: Wind Speed Distribution
    st.subheader("Wind Speed Distribution")
    fig, ax = plt.subplots()
    sns.histplot(data=data["wind_kph"], bins=20, kde=True, ax=ax)
    ax.set_title("Wind Speed Distribution (kph)")
    st.pyplot(fig)

    # Visualization 5: Condition Frequency
    st.subheader("Weather Condition Frequency")
    fig, ax = plt.subplots()
    sns.countplot(data=data, y="condition.text", ax=ax, order=data["condition.text"].value_counts().index)
    ax.set_title("Frequency of Weather Conditions")
    st.pyplot(fig)
