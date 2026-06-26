from flask import Blueprint, render_template, request
from services import opensky_service

airport_bp = Blueprint('airport', __name__)

AIRPORTS = {
    'BLR': 'Kempegowda Intl · Bengaluru',
    'DEL': 'Indira Gandhi Intl · Delhi',
    'BOM': 'Chhatrapati Shivaji Intl · Mumbai',
    'MAA': 'Chennai Intl',
    'HYD': 'Rajiv Gandhi Intl · Hyderabad',
}

@airport_bp.route('/airports')
def airports():
    code = request.args.get('code', 'BLR').upper()
    if code not in AIRPORTS:
        code = 'BLR'
    radius = int(request.args.get('radius', 50))
    traffic = opensky_service.get_airport_traffic(code, radius_km=radius)
    avg_alt = round(sum(f['altitude'] or 0 for f in traffic) / len(traffic)) if traffic else 0
    avg_spd = round(sum(f['speed'] or 0 for f in traffic) / len(traffic)) if traffic else 0
    return render_template('airports.html',
                           airports=AIRPORTS, code=code,
                           name=AIRPORTS[code], traffic=traffic,
                           avg_alt=avg_alt, avg_spd=avg_spd, radius=radius)
