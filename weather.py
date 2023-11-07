import argparse
import sys
import json
from pprint import pp
from configparser import ConfigParser
from urllib import parse, request, error


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
        nargs="+",              # need at least 1 city
        type = str,
        help = "City name. Format: '<City name>, <Country Code>"
    )

    parser.add_argument(
        "-i",
        "--imperial",
        action = "store_true",
        help = "change unit to imperial units"
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
    city_name = " ".join(city_input)
    # print(city_name)
    url_encoded_city_name = parse.quote_plus(city_name)
    # print(url_encoded_city_name)
    units = "imperial" if imperial else "metric"
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
        elif http_error.code == 404: # 404 - Not found
            sys.exit("Cannot find weather for this city.")
        else:
            sys.exit("Something went wrong... ({http_code.code})")
    data = response.read()

    try:
        return json.loads(data)
    except:
        sys.exit("Couldn't read server response.")

def display_weather_info(weather_data, imperial = False):
    """Prints formatted weather information about a city.
    
    Args:
        weather_data (dict): API response from OpenWeather by city name
        imperial (bool): Whether or not to use imperial units for temperature
        
        More information at https://openweathermap.org/current#name"""

if __name__ == "__main__":
    user_args = read_user_cli_args()
    print(user_args)
    query_url = build_weather_query(user_args.city, user_args.imperial)
    print(query_url)
    weather_data = get_weather_data(query_url)
    pp(weather_data)
