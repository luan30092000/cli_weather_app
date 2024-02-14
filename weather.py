import argparse
import sys
import json
from pprint import pp
from configparser import ConfigParser
from urllib import parse, request, error
from datetime import datetime


BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

def _get_api_key():
    """Fetch the API key from configuration file.
    
    Expects a configuration file named "secrets.ini" with structure:

        [openweather]
        api_key = <API KEY>
    """
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"] 

def read_user_cli_args():
    """Handles the CLI user interactions.
    
    Return:
        argparse.Namespace: Populated namespace object
    """

    parser = argparse.ArgumentParser(description="Get weather and temperature information for a city")

    parser.add_argument(
        "city",                 
        nargs="+",          # city name can have multiple words
        type = str,         # city name is a string
        help = "City name. Format: '<City name>, <Country Code>"
    )

    parser.add_argument(
        "-i",
        "--imperial",
        action = "store_true",
        help = "display the temperature in imperial units (Fahrenheit), default is metric (Celsius)",
    )

    parser.add_argument(
        "-a",
        "--all",
        action = "store_true",
        help = "display all weather information, default is to display a pretty summary",
    )

    return parser.parse_args()

def build_weather_query(city_input, imperial = False):
    """Build the URL for an API request to OpenWeather's weather API.
    
    Args: 
        city_input (List[str]): Name of a city as collected by argparse
        imperial (bool): Whether or not to use imperial units for temperature 
        
    Return:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    api_key = _get_api_key()
    city_name = " ".join(city_input)                    # Join the list of city name words into a single string e.g. ["New", "York"] -> "New York"
    url_encoded_city_name = parse.quote_plus(city_name) # URL encode city name e.g. "New York" -> "New+York"
    units = "imperial" if imperial else "metric"        # Use imperial units if requested
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url

def get_weather_data(query_url):
    """Make an API request to a URL and returns the data as a Python object.
    
    Args:
        query_url (str):URL formatted for OpenWeather's city name endpoint
        
    Return:
        dict: Weather information for a specific city
    """
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401: # 401 - Unauthorized
            sys.exit("Access denied. Check API key.")
        elif http_error.code == 404: # 404 - Not Found
            sys.exit("Cannot find weather for this city.")
        else:
            sys.exit("Something went wrong... ({http_code.code})")
    data = response.read()

    try:
        return json.loads(data)
    except:
        sys.exit("Couldn't read server response.")

def display_all_weather_info(weather_data, imperial = False):
    """Prints formatted weather information about a city.
    
    Args:
        weather_data (dict): API response from OpenWeather by city name
        imperial (bool): Whether or not to use imperial units for temperature
        
        More information at https://openweathermap.org/current#name"""
    
    city = weather_data["name"]
    country = weather_data["sys"]["country"]
    description = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
    temp_min = weather_data["main"]["temp_min"]
    temp_max = weather_data["main"]["temp_max"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    wind_deg = weather_data["wind"]["deg"]
    visibility = weather_data["visibility"]
    sunrise = weather_data["sys"]["sunrise"]
    sunrise = datetime.fromtimestamp(sunrise).strftime("%H:%M:%S")
    sunset = weather_data["sys"]["sunset"]
    sunset = datetime.fromtimestamp(sunset).strftime("%H:%M:%S")

    print(f"{REVERSE}Weather in {city}, {country}{RESET}")
    print(f"Status: {description}")
    print(f"Temperature: {temp}°{'F' if imperial else 'C'}")
    print(f"Feels like: {feels_like}°{'F' if imperial else 'C'}")
    print(f"Min temperature: {temp_min}°{'F' if imperial else 'C'} Max temperature: {temp_max}°{'F' if imperial else 'C'}")
    print(f"Humidity: {humidity}%")
    print(f"Wind: {wind_speed} m/s, {wind_deg}°")
    print(f"Visibility: {visibility} m")
    print(f"Sunrise: {sunrise}, Sunset: {sunset}")

PADDING = 20
REVERSE = "\033[;7m"
RESET = "\033[0m"

def display_pretty_weather_info(weather_data, imperial = False):
    city = weather_data["name"]
    description = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
    sunrise = weather_data["sys"]["sunrise"]
    sunrise = datetime.fromtimestamp(sunrise).strftime("%H:%M:%S")
    sunset = weather_data["sys"]["sunset"]
    sunset = datetime.fromtimestamp(sunset).strftime("%H:%M:%S")

    print(f"{REVERSE}{city:^{PADDING}}{RESET}", end="")
    print(
        f"\t{description.capitalize():^{PADDING}}",
        end=" ",
    )
    print(f"({temp}°{'F' if imperial else 'C'})")

def display_weather_info(weather_data, imperial = False, all = False):
    if all:
        display_all_weather_info(weather_data, imperial)
    else:
        display_pretty_weather_info(weather_data, imperial)
if __name__ == "__main__":
    user_args = read_user_cli_args()    # Read user input from the command line
    query_url = build_weather_query(user_args.city, user_args.imperial) # Build the URL for the API request
    weather_data = get_weather_data(query_url)  # Make the API request and get the data
    display_weather_info(weather_data, user_args.imperial, user_args.all) # Display the weather information
