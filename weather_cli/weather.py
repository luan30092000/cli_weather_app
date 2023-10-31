import argparse
import pyfiglet
from simple_chalk import chalk
import requests

# API key for openweathermap
API_KEY = "f67b12ec4904d1ff7c45001e43f61246"

# Base on URL for openweathermap API
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Mapping weather codes to weather icons
WEATHER_ICONS = {
    # day icons
    "01d": "☀️",
    "02d": "⛅️",
    "03d": "☁️",
    "04d": "☁️",
    "09d": "🌧",
    "10d": "🌦",
    "11d": "⛈",
    "13d": "🌨",
    "50d": "🌫",
    # night icons
    "01n": "🌙",
    "02n": "☁️",
    "03n": "☁️",
    "04n": "☁️",
    "09n": "🌧",
    "10n": "🌦",
    "11n": "⛈",
    "13n": "🌨",
    "50n": "🌫",
}


# Making API url with query parameters
parser = argparse.ArgumentParser(description="Check the weather for a certain country/city")
parser.add_argument("country", help="The country/city to check the weather for")
args = parser.parse_args()
url = f"{BASE_URL}?q={args.country}&appid={API_KEY}&units=metric"


# Make API request and parse response using requests module
response = requests.get(url)
if response.status_code != 200:
    print(chalk.red("Error: Unable to retrieve weather information"))
    exit()

# Parsing the JSON response from API and extract weather information
data = response.json()

# Get information from response
temperature = data["main"]["temp"]
feels_like = data["main"]["feels_like"]
description = data["weather"][0]["description"]
icon = data["weather"][0]["icon"]
city = data["name"]
country = data["sys"]["country"]

# Construct output with weather icon
weather_icon = WEATHER_ICONS.get(icon, "")
output = f"Location: {city}, {country}\n"
output += f"Condition: {description}\n"
output += f"Temperature: {temperature}°C; "
output += f"feels like: {feels_like}°C\n"

print(chalk.green(output))