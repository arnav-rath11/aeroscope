from flask import Blueprint, jsonify, request
from models import db, Aircraft, PositionHistory
from services import opensky_service
from datetime import datetime

api_bp = Blueprint('api', __name__)


def _save_flights(flights):
    """Persist fetched flights to the database."""
    for f in flights:
        icao = f.get('icao24', '').lower()
        if not icao:
            continue
        ac = Aircraft.query.filter_by(icao24=icao).first()
        if not ac:
            ac = Aircraft(icao24=icao, callsign=f.get('callsign'))
            db.session.add(ac)
            db.session.flush()
        else:
            ac.callsign = f.get('callsign') or ac.callsign
            ac.updated_at = datetime.utcnow()

        if f.get('latitude') and f.get('longitude'):
            pos = PositionHistory(
                aircraft_id=ac.id,
                latitude=f['latitude'],
                longitude=f['longitude'],
                altitude=f.get('baro_altitude'),
                velocity=f.get('velocity'),
                heading=f.get('heading'),
                vertical_rate=f.get('vertical_rate'),
                on_ground=f.get('on_ground', False),
            )
            db.session.add(pos)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()


@api_bp.route('/flights')
def flights():
    data = opensky_service.get_flights()
    _save_flights(data)
    return jsonify({'count': len(data), 'aircraft': data})


@api_bp.route('/stats')
def stats():
    flights = opensky_service.get_flights()
    airborne = [f for f in flights if not f.get('on_ground')]
    avg_alt = round(sum(f['altitude'] or 0 for f in airborne) / len(airborne)) if airborne else 0
    avg_spd = round(sum(f['speed'] or 0 for f in airborne) / len(airborne)) if airborne else 0
    return jsonify({
        'total': len(flights),
        'airborne': len(airborne),
        'avg_altitude_ft': avg_alt,
        'avg_speed_kts': avg_spd,
        'updated_at': datetime.utcnow().isoformat(),
    })


@api_bp.route('/aircraft/<icao24>')
def aircraft(icao24):
    data = opensky_service.get_aircraft(icao24)
    if not data:
        return jsonify({'error': 'Aircraft not found or offline'}), 404
    return jsonify(data)


@api_bp.route('/history/<icao24>')
def history(icao24):
    ac = Aircraft.query.filter_by(icao24=icao24.lower()).first()
    if not ac:
        return jsonify({'error': 'No history for this aircraft'}), 404
    limit = min(int(request.args.get('limit', 200)), 500)
    positions = ac.positions.order_by(PositionHistory.timestamp.desc()).limit(limit).all()
    return jsonify({
        'icao24': icao24,
        'callsign': ac.callsign,
        'positions': [p.to_dict() for p in reversed(positions)],
    })


@api_bp.route('/airport/<code>')
def airport(code):
    radius = int(request.args.get('radius', 50))
    traffic = opensky_service.get_airport_traffic(code.upper(), radius_km=radius)
    avg_alt = round(sum(f['altitude'] or 0 for f in traffic) / len(traffic)) if traffic else 0
    avg_spd = round(sum(f['speed'] or 0 for f in traffic) / len(traffic)) if traffic else 0
    return jsonify({
        'airport': code.upper(),
        'radius_km': radius,
        'count': len(traffic),
        'avg_altitude_ft': avg_alt,
        'avg_speed_kts': avg_spd,
        'aircraft': traffic,
    })
