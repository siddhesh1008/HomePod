import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key and city from .env file
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Berlin")  # Default to Berlin if not set
COUNTRY_CODE = os.getenv("COUNTRY_CODE", "DE")  # Default to Germany
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str = CITY):
    """
    Fetch current weather for a given city.

    Args:
        city (str): Name of the city to get weather for.

    Returns:
        str: Weather details in a formatted response.
    """
    if not API_KEY:
        return "Weather service is unavailable. API key is missing."

    params = {
        "q": f"{city},{COUNTRY_CODE}",
        "appid": API_KEY,
        "units": "metric",  # Fetch temperature in Celsius
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data["cod"] != 200:
            return f"Sorry, I couldn't find weather data for {city}."

        weather_desc = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_report = (
            f"🌍 Weather in {city}:\n"
            f"🌡 Temp: {temperature}°C\n"
            f"🌦 Condition: {weather_desc}\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind Speed: {wind_speed} m/s"
        )

        return weather_report

    except requests.exceptions.RequestException:
        return "I couldn't fetch the weather right now. Please check your internet connection."
