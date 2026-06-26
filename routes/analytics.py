from flask import Blueprint, render_template
from models import db, Aircraft, PositionHistory
from datetime import datetime, timedelta
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def analytics():
    now = datetime.utcnow()
    # Hourly counts for last 24h
    hourly = []
    for i in range(23, -1, -1):
        start = now - timedelta(hours=i+1)
        end = now - timedelta(hours=i)
        count = db.session.query(func.count(PositionHistory.id))\
            .filter(PositionHistory.timestamp.between(start, end)).scalar()
        hourly.append({'hour': start.strftime('%H:00'), 'count': count or 0})

    total_aircraft = Aircraft.query.count()
    total_positions = PositionHistory.query.count()

    return render_template('analytics.html',
                           hourly=hourly,
                           total_aircraft=total_aircraft,
                           total_positions=total_positions)
