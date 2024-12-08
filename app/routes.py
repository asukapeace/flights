from flask import render_template, request
from app import app 
from opensky_api import OpenSkyApi
import requests
from datetime import datetime, timedelta
import json
def _getAPI():
    return OpenSkyApi()

@app.route('/', methods=['GET'])
def front_page():
    #TODO put more here
    return render_template('index.html', data={'Message' : 'Welcome to my page about flights'})

@app.route('/departures', methods=['GET'])
def departures():
    # for now use heathrow as default
    # TODO find out how to map to the ICAO code

    now = datetime.now()
    airport = request.args.get('icao', 'EGLL')
    start_time = int(request.args.get('begin', (now - timedelta(minutes = 30)).timestamp()))
    end_time = int(request.args.get('end', (now + timedelta(minutes = 30)).timestamp()))

    departures = _getAPI().get_departures_by_airport(airport, start_time, end_time)
    headers = departures[0].__dict__.keys()

    data=[]
    for d in departures:
        flightInfo = {}
        flightInfo['ICAO'] =  d.icao24
        flightInfo['Call sign'] = d.callsign
        flightInfo['Estimated horiz distance from dep airport'] = d.estDepartureAirportHorizDistance
        flightInfo['Estimated vert distance from dep airport'] = d.estDepartureAirportVertDistance
        flightInfo['Estimated arrival airport'] = d.estArrivalAirport
        flightInfo['Time last seen'] = datetime.fromtimestamp(d.lastSeen).strftime('%Y-%m-%d %H:%M:%S') if d.lastSeen else d.lastSeen
        data.append(flightInfo)
    return render_template('flight_info.html', data=data)