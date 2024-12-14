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

def _formatRequestDates(d):
    return int(datetime.strptime(d, "%Y-%m-%dT%H:%M").timestamp())

def _queryAndProcess(requestArgs, func):
    """
    handles the request from the query page (arrivals or departures)
    """
    airport = requestArgs.get('icao')
    start_time = _formatRequestDates(requestArgs.get('begin'))
    end_time = _formatRequestDates(requestArgs.get('end'))

    response = func(airport, start_time, end_time)
    data=[]
    if response:
        for d in response:
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
    """ returns dict of arrivals info for given airport and timerange"""
    return _queryAndProcess(request.args, _getAPI().get_arrivals_by_airport)

@app.route('/departures', methods=['GET'])
def departures():
    """ returns dict of departure info for given airport and timerange"""
    return _queryAndProcess(request.args, _getAPI().get_departures_by_airport)

@app.route('/aircraft', methods=['GET'])
def aircraft():
    icao24 = request.args.get('icao24')
    begin = _formatRequestDates(request.args.get('begin'))
    end = _formatRequestDates(request.args.get('end'))
    data = _getAPI().get_flights_by_aircraft(icao24, begin, end)
    return render_template('aircraft.html', data=data)