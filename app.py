import streamlit as st
from meteostat import Point, Daily
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Streamlit 페이지 설정
st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️", layout="wide")

# Streamlit UI 구성
st.title("🌤️ Weather Dashboard")

# 도시 설정
city_name = st.selectbox(
    "Select City:",
    ["Seoul", "New York", "London", "Tokyo", "Sydney"],
    index=0
)
start_date = st.date_input("Start:", value=datetime.date(2024, 12, 1))
end_date = st.date_input("End:", value=datetime.date(2024, 12, 10))

# 도시 좌표
city_coordinates = {
    "Seoul": (37.5665, 126.9780),
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6895, 139.6917),
    "Sydney": (-33.8688, 151.2093)
}

# 선택한 도시의 좌표 가져오기
latitude, longitude = city_coordinates[city_name]

#데이터 요청 및 처리
def fetch_weather_data(lat, lon, start, end):
    location = Point(lat, lon)

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    data = Daily(location, start, end)
    data = data.fetch()

    return data.reset_index()

#데이터 가져오기
if st.button("Weather Data Check"):
    if start_date > end_date:
        st.error("The end date must be after the start date.")
    else:
        weather_data = fetch_weather_data(latitude, longitude, start_date, end_date)

        if weather_data.empty:
            st.warning("There is no data for that period.")
        else:
            st.subheader(f"📊 {city_name} Weather Data ({start_date} ~ {end_date})")
            st.dataframe(weather_data)

            fig, ax = plt.subplots(figsize=(10, 4))

            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
            ax.plot(weather_data['time'], weather_data['tavg'], label="Avg Temp (°C)", color="blue", linewidth=2)
            ax.bar(weather_data['time'], weather_data['prcp'], label="PRCP (mm)", color="cyan", alpha=0.6)
            ax.set_title(f"{city_name} Weather", fontsize=16)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Temp (°C) / Prcp (mm)", fontsize=12)
            ax.legend(fontsize=10)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
            plt.grid(alpha=0.3)

            st.pyplot(fig)

            st.metric("Average Temperature", f"{weather_data['tavg'].mean():.2f}°C")
            st.metric("Precipitation", f"{weather_data['prcp'].sum():.2f} mm")