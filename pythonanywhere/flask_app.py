from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/forecastLatLon')
@app.route('/forecastLatLon/<lat>')
@app.route('/forecastLatLon/<lat>/<lon>')
def forecast_lat_lon(lat="", lon=""):
    import modules.forecastLatLon as forecast
    return forecast.week(lat, lon)


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response
