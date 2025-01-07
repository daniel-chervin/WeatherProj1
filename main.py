
import streamlit as st
from streamlit_folium import st_folium
import folium

from helper_functions import *

# Streamlit App
st.set_page_config(layout="wide")
st.title("Select on World Map to Retrieve City Weather")
st.write("**Click on the map** to retrieve the city name for the selected location, or search for a city to focus on it then click to display the data.")

# Layout with 1 row and 2 columns
row1_col1, row1_col2 = st.columns([2, 1])

#location_data = get_current_location_by_ip()
gg = geocoder.ip('me')
lat = -999.9; lon = -999.9
city_name = get_city_from_coords(lat, lon)
if gg.ok:
    lat = gg.latlng[0] if gg.latlng else -999.9
    lon = gg.latlng[1] if gg.latlng else -999.9
    city_name = gg.city



# Create a Folium map in the left column
with row1_col1:
    #lat = 32.084
    #lon = 34.779
    #city_name = get_city_from_coords(lat, lon)
    map_center = [lat, lon ]  # Default center of the map (latitude, longitude)
    zoom_start = 12  # Default zoom level

    # City search input
    city_search = st.text_input("Search for a city:")
    if city_search:
        coords = get_coords_from_city(city_search)
        if coords:
            map_center = [coords[0], coords[1]]
            lat = coords[0]; lon = coords[1]
            zoom_start = 12
        else:
            st.write("City not found. Please try another city.")

    # Initialize map with updated center
    m = folium.Map(location=map_center, zoom_start=zoom_start)

    # Add marker if city is found
    if city_search and coords:
        folium.Marker(location=coords, popup=city_search).add_to(m)
    elif is_valid_lat_lon(lat, lon):
        folium.Marker(location=[lat, lon], popup=city_search).add_to(m)
    # Add Folium map to Streamlit
    map_data = st_folium(m, width=700, height=500)

# Display selected location and city name in the right column
with row1_col2:
    st.write("### Selected Location and City")
    if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
        last_clicked = map_data["last_clicked"]
        lat = last_clicked["lat"]
        lon = last_clicked["lng"]

    if is_valid_lat_lon(lat, lon):
        city_name = get_city_from_coords(lat, lon)
        st.write(f"**City Name:** {city_name}")
        st.write(f"**Lat, Lon:** {lat:.3f}, {lon:.3f}")
        #st.write(f"**Longitude:** {lon:.3f}")
        #city_search.title(city_name)
        local_dt = get_local_datetime(lat, lon)
        st.write(f"**Local date time:** {local_dt}")

        #weather_data = get_weather_data(city_name)
        location = f"{lat},{lon}"
        weather_data = get_weather_data(location, 'current')

        #print(type(weather_data))

        if "error" in weather_data:
            st.write(f"**Error:** {weather_data['error']}")
        else:
            # Extract and display relevant weather details
            print("\nWeather Details:")
            st.write(f"**Location:** {weather_data['location']['name']}, {weather_data['location']['country']}")
            #st.write(f"**Local Time:** {weather_data['location']['localtime']}")
            st.write(f"**Temperature (°C):** {weather_data['current']['temp_c']}")
            st.write(f"**Condition:** {weather_data['current']['condition']['text']}")
            st.write(f"**Feels Like (°C):** {weather_data['current']['feelslike_c']}")
            st.write(f"**Wind Speed (kph):** {weather_data['current']['wind_kph']}")
            st.write(f"**Humidity (%):** {weather_data['current']['humidity']}")
            st.write(f"**Cloud Cover (%):** {weather_data['current']['cloud']}")
            #st.write(f"**City:** {weather_data['location']['name']}")
            #st.write(f"**Region:** {weather_data['location']['region']}")
            #st.write(f"**Country:** {weather_data['location']['country']}")
            #st.write(f"**Temperature:** {weather_data['current']['temp_c']} °C")
            #st.write(f"**Weather:** {weather_data['current']['condition']['text']}")
            #st.write(f"**Humidity:** {weather_data['current']['humidity']}%")
            #st.write(f"**Wind Speed:** {weather_data['current']['wind_kph']} kph")

# Add a second row with two columns
row2_col1, row2_col2 = st.columns([1, 1])
forecast_data = {}
if is_valid_lat_lon(lat, lon):
    location = f"{lat},{lon}"
    forecast_data = get_weather_data(location, 'forecast', 7)

with row2_col1:
    #if city_name.lower() != "city not found":
    if is_valid_lat_lon(lat, lon):
        st.write(f"## 7 days weather Forecast for {city_name}")
        #location = f"{lat},{lon}"
        #forecast_data = get_weather_data(location, 'forecast', 7)
        if "error" in forecast_data:
            st.write(f"**Error:** {forecast_data['error']}")
        else:
            forecast_days = forecast_data["forecast"]["forecastday"]
            forecast_list = []
            for day in forecast_days:
                date = day["date"]
                day_info = day["day"]
                forecast_list.append({
                    "Metric": ["Max Temp (°C)", "Min Temp (°C)", "Condition", "Rain Chance (%)", "Snow Chance (%)"],
                    date: [
                        day_info["maxtemp_c"],
                        day_info["mintemp_c"],
                        day_info["condition"]["text"],
                        day_info.get("daily_chance_of_rain", "N/A"),
                        day_info.get("daily_chance_of_snow", "N/A"),
                    ],
                })

            forecast_df = pd.concat([pd.DataFrame(item).set_index("Metric") for item in forecast_list], axis=1)
            st.table(forecast_df)

with row2_col2:
    #st.write("## Historical Weather Data")
    #st.write("(N/A too cheap to pay for a proper license!)")
    #forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
    if is_valid_lat_lon(lat, lon):
        if "error" in forecast_data:
            st.write(f"**Error:** {forecast_data['error']}")
        else:
            forecast_list = []
            for day in forecast_days:
                forecast_list.append({
                    "Date": day['date'],
                    "Max Temp (°C)": day['day']['maxtemp_c'],
                    "Min Temp (°C)": day['day']['mintemp_c'],
                    "Avg Temp (°C)": day['day']['avgtemp_c'],
                    "Precipitation (mm)": day['day']['totalprecip_mm'],
                    "Condition": day['day']['condition']['text']
                })
            forecast_df = pd.DataFrame(forecast_list)
            st.write("## 7 days Weather trends")
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=forecast_df, x='Date', y='Max Temp (°C)', label='Max Temp (°C)', color='red', ax=ax)
            sns.lineplot(data=forecast_df, x='Date', y='Min Temp (°C)', label='Min Temp (°C)', color='blue', ax=ax)
            sns.barplot(data=forecast_df, x='Date', y='Precipitation (mm)', label='Precipitation (mm)',color='skyblue', ax=ax)

            #sns.lineplot(data=forecast_df, x='Date', y='Avg Temp (°C)', label='Avg Temp (°C)', color='green', ax=ax)
            ax.set_title('Weather Trends')
            ax.set_xlabel('Date')
            ax.grid(True, linestyle='--', alpha=0.6)
            #ax.set_ylabel('Temperature (°C)')
            ax.legend()
            st.pyplot(fig)


