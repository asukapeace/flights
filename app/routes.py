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

@app.route('/departure-query', methods=['GET', 'POST'])
def departure_query():
    return render_template('query.html', data={'departures' : True})

@app.route('/arrivals-query', methods=['GET', 'POST'])
def arrivals_query():
    return render_template('query.html', data={'arrivals' : True})

@app.route('/aircraft-query', methods=['GET', 'POST'])
def aircraft_query():
    return render_template('query.html', data={'aircraft' : True})

@app.route('/current-position-query', methods=['GET', 'POST'])
def current_position_query():
    return render_template('query.html', data={'current_position' : True})

@app.route('/flight-track-query', methods=['GET', 'POST'])
def flight_track_query():
    return render_template('query.html', data={'tracking' : True})

def _format_request_dates(d):
    return int(datetime.strptime(d, "%Y-%m-%dT%H:%M").timestamp())

def _query_and_process(request_args, func):
    """
    handles the request from the query page (arrivals or departures)
    """
    airport = request_args.get('icao')
    start_time = _format_request_dates(request_args.get('begin'))
    end_time = _format_request_dates(request_args.get('end'))

    response = func(airport, start_time, end_time)
    data=[]
    if response:
        for d in response:
            flight_info = {}
            flight_info['ICAO'] =  d.icao24
            flight_info['Call sign'] = d.callsign
            flight_info['Estimated horiz distance from dep airport'] = d.estDepartureAirportHorizDistance
            flight_info['Estimated vert distance from dep airport'] = d.estDepartureAirportVertDistance
            flight_info['Estimated arrival airport'] = d.estArrivalAirport
            flight_info['Time last seen'] = datetime.fromtimestamp(d.lastSeen).strftime('%Y-%m-%d %H:%M:%S') if d.lastSeen else d.lastSeen
            data.append(flight_info)
    return render_template('flight_info.html', data=data)

@app.route('/arrivals', methods=['GET'])
def arrivals():
    """ returns dict of arrivals info for given airport and timerange"""
    return _query_and_process(request.args, _getAPI().get_arrivals_by_airport)

@app.route('/departures', methods=['GET'])
def departures():
    """ returns dict of departure info for given airport and timerange"""
    return _query_and_process(request.args, _getAPI().get_departures_by_airport)

@app.route('/aircraft', methods=['GET'])
def aircraft():
    icao24 = request.args.get('icao24')
    begin = _format_request_dates(request.args.get('begin'))
    end = _format_request_dates(request.args.get('end'))
    data = _getAPI().get_flights_by_aircraft(icao24, begin, end)
    flights = []
    for flight in data:
        flight_info = {
            'icao24': flight.icao24,
            'callsign': flight.callsign,
            'estDepartureAirportHorizDistance': flight.estDepartureAirportHorizDistance,
            'estDepartureAirportVertDistance': flight.estDepartureAirportVertDistance,
            'estArrivalAirport': flight.estArrivalAirport,
            'lastSeen': flight.lastSeen
        }
        flights.append(flight_info)
    return render_template('aircraft.html', data=flights)

@app.route('/current-position', methods=['GET'])
def current_position():
    icao24 = request.args.get('icao24')
    states = _getAPI().get_states(icao24=icao24)
    if states:
        position = states.states[0].latitude, states.states[0].longitude
    else:
        position = None
    return render_template('track_aircraft.html', icao24=icao24, position=position)

@app.route('/flight-path', methods=['GET'])
def flight_path():
    icao24 = request.args.get('icao24')
    flight_tracks = _getAPI().get_track_by_aircraft(icao24)

    coordinates = []
    for track in flight_tracks.path:
        coordinates.append((track[1], track[2]))

    return render_template('flight_path.html', icao24=icao24, coordinates=coordinates)