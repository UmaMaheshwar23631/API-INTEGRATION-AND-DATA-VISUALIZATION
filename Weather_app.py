import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# --------------------- FUNCTION: Fetch Weather Data ---------------------
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != "200":
            return None, data.get("message", "Error")
        return data, None
    except requests.exceptions.RequestException as e:
        return None, str(e)

# --------------------- FUNCTION: Plot Graph ---------------------
def plot_line_chart(dates, values, title, ylabel, color):
    plt.figure(figsize=(10, 4))
    sns.lineplot(x=dates, y=values, marker='o', color=color)
    plt.title(title, fontsize=14)
    plt.xlabel("Date & Time")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# --------------------- STREAMLIT APP UI ---------------------
st.title("📊 Weather Forecast Dashboard")
st.markdown("Get 5-day weather forecast: Temperature 🌡️, Humidity 💧, Pressure 🌬️")

# Input fields
api_key = st.text_input("🔑 Enter your OpenWeatherMap API Key", type="password")
city = st.text_input("🏙️ Enter City Name", value="Mumbai")                              # Default - Mumbai

if st.button("Fetch Weather Data"):
    if not api_key or not city:
        st.error("Please enter both API key and city.")
    else:
        data, error = get_weather_data(city, api_key)
        if error:
            st.error(f"❌ {error}")
        else:
            # Extract data from API response
            dates = []
            temps = []
            humidity = []
            pressure = []

            for entry in data['list']:
                time = datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S")
                main = entry['main']
                dates.append(time)
                temps.append(main['temp'])
                humidity.append(main['humidity'])
                pressure.append(main['pressure'])

            # Show plots
            st.subheader("🌡️ Temperature Forecast (°C)")
            plot_line_chart(dates, temps, f"{city} - Temperature Forecast", "Temperature (°C)", "tomato")

            st.subheader("💧 Humidity Forecast (%)")
            plot_line_chart(dates, humidity, f"{city} - Humidity Forecast", "Humidity (%)", "royalblue")

            st.subheader("🌬️ Pressure Forecast (hPa)")
            plot_line_chart(dates, pressure, f"{city} - Pressure Forecast", "Pressure (hPa)", "seagreen")
