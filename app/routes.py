from flask import render_template, request
from app import app 
from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import json
def _getAPI():
    return OpenSkyApi()

@app.route('/', methods=['GET'])
def front_page():
    #TODO put more here
    return render_template('index.html', data={'Message' : 'Welcome to my page about flights'})

@app.route('/departureQuery', methods=['GET', 'POST'])
def departureQuery():
    return render_template('query.html', data={'departures' : True})

@app.route('/arrivalsQuery', methods=['GET', 'POST'])
def arrivalsQuery():
    return render_template('query.html', data={'arrivals' : True})

def _queryAndProcess(requestArgs, func):
    # TODO find out how to map to the ICAO code
/*************  ✨ Codeium Command ⭐  *************/
    """
    Handles the POST requests from the query forms.

    requestArgs: the GET request arguments
    func: the function to call to get the data

    :return: a rendered template with the data
    """
/******  62c5b124-e09e-410f-bdb2-38d72fb14325  *******/
    airport = requestArgs.get('icao')
    start_time = int(datetime.strptime(requestArgs.get('begin'), "%Y-%m-%dT%H:%M").timestamp())
    end_time = int(datetime.strptime(requestArgs.get('end'), "%Y-%m-%dT%H:%M").timestamp())

    departures = func(airport, start_time, end_time)
    data=[]
    if departures:
        headers = departures[0].__dict__.keys()

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

@app.route('/arrivals', methods=['GET'])
def arrivals():
    return _queryAndProcess(request.args, _getAPI().get_arrivals_by_airport)

@app.route('/departures', methods=['GET'])
def departures():
    return _queryAndProcess(request.args, _getAPI().get_departures_by_airport)