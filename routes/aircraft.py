from flask import Blueprint, render_template, request, jsonify, abort
from models import db, Aircraft, PositionHistory
from services import opensky_service

aircraft_bp = Blueprint('aircraft', __name__)

@aircraft_bp.route('/map')
def live_map():
    return render_template('map.html')

@aircraft_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = []
    if query:
        results = opensky_service.search_by_callsign(query)
    return render_template('search.html', query=query, results=results)

@aircraft_bp.route('/aircraft/<icao24>')
def detail(icao24):
    live = opensky_service.get_aircraft(icao24)
    ac = Aircraft.query.filter_by(icao24=icao24.lower()).first()
    history = []
    if ac:
        history = ac.positions.order_by(PositionHistory.timestamp.desc()).limit(200).all()
    return render_template('aircraft_detail.html',
                           icao24=icao24, live=live,
                           aircraft=ac, history=history)
