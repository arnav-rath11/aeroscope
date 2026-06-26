import os
import math
import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

OPENSKY_API_URL = 'https://opensky-network.org/api'
OPENSKY_USERNAME = os.environ.get('OPENSKY_USERNAME', '')
OPENSKY_PASSWORD = os.environ.get('OPENSKY_PASSWORD', '')

# India bounding box (default region)
DEFAULT_BBOX = {
    'lamin': 6.0, 'lamax': 37.0,
    'lomin': 68.0, 'lomax': 97.0,
}

AIRPORT_COORDS = {
    'BLR': (13.1979, 77.7063),
    'DEL': (28.5562, 77.1000),
    'BOM': (19.0896, 72.8656),
    'MAA': (12.9941, 80.1709),
    'HYD': (17.2403, 78.4294),
}


def _auth():
    if OPENSKY_USERNAME and OPENSKY_PASSWORD:
        return (OPENSKY_USERNAME, OPENSKY_PASSWORD)
    return None


def _ms_to_knots(ms):
    return round(ms * 1.94384, 1) if ms is not None else None


def _m_to_ft(m):
    return round(m * 3.28084) if m is not None else None


def get_flights(bbox=None):
    """Fetch all aircraft states in a bounding box. Returns list of dicts."""
    params = bbox or DEFAULT_BBOX
    try:
        resp = requests.get(
            f'{OPENSKY_API_URL}/states/all',
            params=params,
            auth=_auth(),
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        states = data.get('states') or []
        return [_parse_state(s) for s in states if s[5] and s[6]]
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            logger.warning('OpenSky rate limit hit')
        else:
            logger.error('OpenSky HTTP error: %s', e)
    except Exception as e:
        logger.error('OpenSky fetch error: %s', e)
    return []


def get_aircraft(icao24):
    """Fetch single aircraft by ICAO24."""
    try:
        resp = requests.get(
            f'{OPENSKY_API_URL}/states/all',
            params={'icao24': icao24.lower()},
            auth=_auth(),
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        states = data.get('states') or []
        if states:
            return _parse_state(states[0])
    except Exception as e:
        logger.error('OpenSky single aircraft error: %s', e)
    return None


def search_by_callsign(callsign):
    """Search flights and filter by callsign substring."""
    all_flights = get_flights()
    cs = callsign.strip().upper()
    return [f for f in all_flights if f['callsign'] and cs in f['callsign'].upper()]


def get_airport_traffic(code, radius_km=50):
    """Get aircraft within radius_km of airport."""
    if code not in AIRPORT_COORDS:
        return []
    lat, lon = AIRPORT_COORDS[code]
    deg = radius_km / 111.0
    bbox = {
        'lamin': lat - deg, 'lamax': lat + deg,
        'lomin': lon - deg, 'lomax': lon + deg,
    }
    flights = get_flights(bbox)
    # Filter to exact radius
    nearby = []
    for f in flights:
        if f['latitude'] and f['longitude']:
            dist = _haversine(lat, lon, f['latitude'], f['longitude'])
            if dist <= radius_km:
                f['distance_km'] = round(dist, 1)
                nearby.append(f)
    return nearby


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _parse_state(s):
    """Parse OpenSky state vector into clean dict."""
    return {
        'icao24': s[0],
        'callsign': (s[1] or '').strip() or None,
        'origin_country': s[2],
        'time_position': s[3],
        'last_contact': s[4],
        'longitude': s[5],
        'latitude': s[6],
        'baro_altitude': _m_to_ft(s[7]),
        'geo_altitude': _m_to_ft(s[13]),
        'on_ground': s[8],
        'velocity': _ms_to_knots(s[9]),
        'heading': round(s[10], 1) if s[10] is not None else None,
        'vertical_rate': round(s[11] * 196.85) if s[11] else 0,  # fpm
        'squawk': s[14],
        'spi': s[15],
        'position_source': s[16],
        # Convenience aliases
        'altitude': _m_to_ft(s[7]),
        'speed': _ms_to_knots(s[9]),
    }
