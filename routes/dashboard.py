from flask import Blueprint, render_template
from models import db, Aircraft, PositionHistory
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    # Recent activity from DB
    cutoff = datetime.utcnow() - timedelta(hours=24)
    total_tracked = db.session.query(Aircraft).count()
    recent_positions = db.session.query(PositionHistory)\
        .filter(PositionHistory.timestamp >= cutoff).count()
    return render_template('dashboard.html',
                           total_tracked=total_tracked,
                           recent_positions=recent_positions)
