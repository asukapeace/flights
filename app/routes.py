from flask import render_template, request
from app import app 
from opensky_api import OpenSkyApi
import requests
from datetime import datetime, timedelta

def _getAPI():
    return OpenSkyApi()

@app.route('/', methods=['GET'])
def front_page():
    #TODO put more here
    return render_template('index.html', data={'Message' : 'Welcome to my page about flights'})

@app.route('/departures', methods=['GET'])
def arrivals():
    # for now use heathrow as default
    # TODO find out how to map to the ICAO code

    now = datetime.now()
    airport = request.args.get('icao', 'EGLL')
    start_time = int(request.args.get('begin', now.timestamp()))
    end_time = int(request.args.get('end', (now + timedelta(minutes = 10)).timestamp()))

    departures = _getAPI().get_departures_by_airport(airport, start_time, end_time)
    return render_template('flight_info.html', data=departures)