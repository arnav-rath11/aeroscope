# AeroScope ✈️

Real-time flight tracking and airspace analytics platform built with Flask, Leaflet.js, and the OpenSky Network API.

## Features

- **Live Map** — interactive Leaflet map with 15-second auto-refresh
- **Aircraft detail** — flight trail visualization from position history
- **Airport monitor** — track traffic around BLR, DEL, BOM, MAA, HYD
- **Analytics** — hourly activity charts, altitude distribution
- **Search** — callsign / ICAO24 lookup
- **Dark/light mode** — persisted via localStorage
- **REST API** — `/api/flights`, `/api/stats`, `/api/aircraft/<icao24>`, `/api/history/<icao24>`, `/api/airport/<code>`

## Quick Start

```bash
# Clone / unzip the project
cd aeroscope

# Create virtual environment
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenSky credentials (optional)

# Run
flask run
# or
python app.py
```

Open http://localhost:5000

## Deploy to Render

1. Push to GitHub
2. Create a new **Web Service** on [render.com](https://render.com)
3. Connect your repo
4. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
5. Add environment variables:
   - `SECRET_KEY` (generate a random string)
   - `OPENSKY_USERNAME` (optional)
   - `OPENSKY_PASSWORD` (optional)
6. Deploy!

For PostgreSQL: add a Render Postgres database and set `DATABASE_URL`.

## Project Structure

```
aeroscope/
├── app.py                  # Flask application factory
├── models.py               # SQLAlchemy models (Aircraft, PositionHistory)
├── services/
│   └── opensky_service.py  # OpenSky API integration
├── routes/
│   ├── dashboard.py
│   ├── aircraft.py
│   ├── analytics.py
│   ├── airport.py
│   └── api.py              # REST API endpoints
├── templates/
│   ├── base.html           # Layout with nav, sidebar
│   ├── dashboard.html
│   ├── map.html
│   ├── search.html
│   ├── aircraft_detail.html
│   ├── analytics.html
│   └── airports.html
├── static/
│   ├── css/main.css        # Dark aviation theme
│   └── js/main.js          # Theme toggle, Chart.js config
├── requirements.txt
├── render.yaml
└── .env.example
```

## API Reference

| Endpoint | Description |
|---|---|
| `GET /api/flights` | All active aircraft in region |
| `GET /api/stats` | Dashboard statistics |
| `GET /api/aircraft/<icao24>` | Single aircraft live data |
| `GET /api/history/<icao24>` | Historical positions (JSON) |
| `GET /api/airport/<code>` | Airport area traffic |

## OpenSky Note

Anonymous access: ~100 requests/day. Register free at opensky-network.org for higher limits (1000+/day). Set `OPENSKY_USERNAME` and `OPENSKY_PASSWORD` in your environment.
