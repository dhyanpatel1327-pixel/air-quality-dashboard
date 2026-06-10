import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from config import API_KEY  
BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

def get_coordinates(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    return None, None

def get_aqi_data(lat, lon):
    url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_aqi_label(aqi):
    labels = {1: "Good 🟢", 2: "Fair 🟡", 3: "Moderate 🟠", 4: "Poor 🔴", 5: "Very Poor ⚫"}
    return labels.get(aqi, "Unknown")

def show_dashboard(city):
    print(f"\n🔍 Fetching air quality data for {city}...")
    lat, lon = get_coordinates(city)
    if not lat:
        print("❌ City not found!")
        return

    data = get_aqi_data(lat, lon)
    components = data['list'][0]['components']
    aqi = data['list'][0]['main']['aqi']

    print(f"\n📍 City: {city}")
    print(f"🌫️  AQI: {aqi} — {get_aqi_label(aqi)}")
    print(f"📊 PM2.5: {components['pm2_5']} μg/m³")
    print(f"📊 PM10:  {components['pm10']} μg/m³")
    print(f"📊 CO:    {components['co']} μg/m³")
    print(f"📊 NO2:   {components['no2']} μg/m³")
    print(f"📊 O3:    {components['o3']} μg/m³")

    # Graph banana
    pollutants = ['PM2.5', 'PM10', 'CO', 'NO2', 'O3']
    values = [components['pm2_5'], components['pm10'],
              components['co']/100, components['no2'], components['o3']]
    colors = ['#FF6B6B', '#FF8E53', '#FFC300', '#36D1DC', '#5B86E5']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(pollutants, values, color=colors, edgecolor='white', linewidth=1.5)
    plt.title(f'Air Quality Dashboard — {city}\nAQI: {aqi} ({get_aqi_label(aqi)})',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Pollutants', fontsize=12)
    plt.ylabel('Concentration (μg/m³)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)

    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{val:.1f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{city}_air_quality.png', dpi=150)
    plt.show()
    print(f"\n✅ Graph saved as '{city}_air_quality.png'")

# Cities check karo
cities = [
    "Mumbai", "Delhi", "Ahmedabad", "Surat", "Pune",
    "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Jaipur"
]
for city in cities:
    show_dashboard(city)