#!/usr/bin/python3

"""
This is a simple web server that demostrates how weather APIs work.
"""


import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/hello', methods=['GET'])
def welcome():
    """Default endpoint"""
    return("Hello, there. Are you using the correct endpoint? 🤗")


@app.route('/api/hello', methods=['GET'])
def hello():
    """
    Returns weather condition based on the user's IP address
    """
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.headers.get('X-Forwarded_For', request.remote_addr)

    location, temperature = location_and_temperature(client_ip)

    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}"
    }
    return jsonify(response)


def location_and_temperature(client_ip):
    """
    Uses the IP address of the user to detect the geolocation and weather,
    through third-party applications
    """
    api_key = "d69ae1406b194ca4ab111ece76c49be5"
    geo_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={client_ip}'
    response = requests.get(geo_url)

    if response.status_code != 200:
        pass

    geo_response = response.json()
    location = geo_response.get("city", "You're living in the bush")

    weather_api = "51c5436ea17c483e90d234559240407"
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api}&q={location}&aqi=no"
    weather_response = requests.get(weather_url).json()
    temperature = weather_response.get("current", {}).get("temp_c", "hawt")

    return location, temperature


if __name__ == '__main__':
    app.run(debug=True)
