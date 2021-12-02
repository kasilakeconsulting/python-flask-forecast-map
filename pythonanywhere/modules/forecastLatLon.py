"""
forecastLatLon.py
This module uses the National Weather Service's APIs to fetch the weather forecast for a lat/lon location in the United States.

Sample URL:
https://kasilakeconsult.pythonanywhere.com/forecastLatLon/38.8894/-77.0352

Successful fetch JSON:
  {
      "result" => "ok",
      "forecasts" => (see below)
  }

Unsuccessful fetch JSON:
  {
      "result" => "error",
      "message" => "error message"
  }

Sample forecast return, first three items:
{
  "result": "ok",
  "forecasts": [
    {
      "number": 1,
      "name": "This Afternoon",
      "startTime": "2021-12-01T17:00:00-05:00",
      "endTime": "2021-12-01T18:00:00-05:00",
      "isDaytime": true,
      "temperature": 73,
      "temperatureUnit": "F",
      "temperatureTrend": "falling",
      "windSpeed": "5 mph",
      "windDirection": "S",
      "icon": "https://api.weather.gov/icons/land/day/few?size=medium",
      "shortForecast": "Sunny",
      "detailedForecast": "Sunny. High near 73, with temperatures falling to around 69 in the afternoon. South wind around 5 mph."
    },
    {
      "number": 2,
      "name": "Tonight",
      "startTime": "2021-12-01T18:00:00-05:00",
      "endTime": "2021-12-02T06:00:00-05:00",
      "isDaytime": false,
      "temperature": 47,
      "temperatureUnit": "F",
      "temperatureTrend": null,
      "windSpeed": "2 mph",
      "windDirection": "NW",
      "icon": "https://api.weather.gov/icons/land/night/sct/fog?size=medium",
      "shortForecast": "Partly Cloudy then Patchy Fog",
      "detailedForecast": "Patchy fog after 3am. Partly cloudy, with a low around 47. Northwest wind around 2 mph."
    },
        {
      "number": 3,
      "name": "Thursday",
      "startTime": "2021-12-02T06:00:00-05:00",
      "endTime": "2021-12-02T18:00:00-05:00",
      "isDaytime": true,
      "temperature": 73,
      "temperatureUnit": "F",
      "temperatureTrend": "falling",
      "windSpeed": "5 mph",
      "windDirection": "NW",
      "icon": "https://api.weather.gov/icons/land/day/fog/few?size=medium",
      "shortForecast": "Patchy Fog then Sunny",
      "detailedForecast": "Patchy fog before 8am. Sunny. High near 73, with temperatures falling to around 69 in the afternoon. Northwest wind around 5 mph."
    },
    ...etc...
  ]

References:
https://weather-gov.github.io/api/general-faqs
https://www.askpython.com/python/examples/pull-data-from-an-api
"""

import requests
import json


def week(lat, lon):
    latLon = lat + "," + lon
    requestURL = "https://api.weather.gov/points/" + latLon
    response_API = requests.get(requestURL)

    '''
    200 : OK. It means we have a healthy connection with the API on web.
    204 : It depicts that we can successfully made a connection to the API, but did not return any data from the service.
    401 : Authentication failed
    403 : Access is forbidden by the API service.
    404 : The requested API service is not found on the server/web.
    500 : Internal Server Error has occurred.
    '''

    if response_API.status_code != 200:
        forecastJSON = {
            "result": "error",
            "message": "Weather API metadata call failed: " + str(response_API.status_code)
        }
    else:
        dataRaw: str = response_API.text

        # Parse the data into JSON format
        dataJSON = json.loads(dataRaw)

        # Get the URL for the general forecast
        requestURL = dataJSON['properties']['forecast']

        response_API = requests.get(requestURL)

        if response_API.status_code != 200:
            forecastJSON = {
                "result": "error",
                "message": "Weather API forecast call failed: " + str(response_API.status_code)
            }
        else:
            dataRaw: str = response_API.text

            # Parse the data into JSON format
            dataJSON = json.loads(dataRaw)

            messageJSON = dataJSON['properties']['periods']

            forecastJSON = {
                "result": "ok",
                "forecasts": messageJSON
            }
            # Parse the data into JSON format
            # dataJSON = json.loads(dataRaw)

    return json.dumps(forecastJSON)


# Provide values if you want to run the module to test it.
if __name__ == '__main__':
    print("Returned from module call:\n" + week("38.8894", "-77.0352"))
