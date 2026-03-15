import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

API_TOKEN = "" #put yours

RSA_KEY = "" #put yours

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def status_code(exclude: str, limit: int = 1):

   if response.status_code == requests.codes.ok:
       return json.loads(response.text)
   else:
        raise InvalidUsage(response.text, status_code=response.status_code)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>Weather: python Saas: 22.02.2026.</h2></p>"


@app.route("/content/api/v1/integration/generate", methods=["POST"])
def weather():
    json_data = request.get_json()
    ur_token = json_data.get("token")
    date = json_data.get("date")
    location = json_data.get("location")
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?key="put your key"&unitGroup=metric'
    response = requests.get(url).json()
    requester_name = json_data.get("requester_name")
    utc_time=dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    result = {
        "requster_name": requester_name,
        "timestamp": utc_time,
        "location" : location,
        "date" : date,
        "weather" :
        {
            "temp_c" : response["days"][0]["temp"],
            "temp_max" : response["days"][0]["tempmax"],
            "temp_min" : response["days"][0]["tempmin"],
            "pressure_mb" : response["days"][0]["pressure"],
            "windspeed_kph" : response["days"][0]["windspeed"],
            "humidity" : response["days"][0]["humidity"]
        }
    }

    return result
