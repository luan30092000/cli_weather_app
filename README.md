# User Manual for weather.py
## Overview
This Python script fetches and displays weather information for a specific city using OpenWeatherAPI.
## Requirements
- Python 3
- An API key from OpenWeatherMap, which should be stored in a configuration file named "secret.ini" in the following format:
```
[openweather]
api_key = <Your API Key>
```
- Installing requirement packages/libraries
```
pip install -r requirements.txt
```

## Usage
You can run the script from the command line with the following syntax:
```
python weather.py <city> [-i] [-a]
```
Arguments
- `<city>`: The name of the city you want to get weather information for. If the city name contains spaces, enclose it in quotes. For example: "New York".
- -i or --imperial: Optional. If this flag is included, the temperature will be displayed in Fahrenheit. If not, the temperature will be displayed in Celsius.
- -a or --all: Optional. If this flag is included, all available weather information will be displayed. If not, only a summary will be displayed.
## Output
The script will print the weather information to the console. The information includes the city name, weather status, temperature, and optionally (if `-a` or `--all` is included), additional information such as humidity, wind speed, visibility, and sunrise/sunset times.
## Error Handling
The script will exit and display an error message if:
- The API key is missing or invalid
- The specified city cannot be found
- There is a problem with the server response
- Any other HTTP error occurs during the API request
## Code Structure
Code Structure
The script is divided into several functions, each with a specific task such as reading user input, building the API request URL, fetching the data, and displaying the results. The main execution of the script is at the bottom, under the if `__name__ == "__main__":` line.

## Demo
![Weather App Demo](demo/Peek%202024-02-13%2020-45.gif)