from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Aircraft(db.Model):
    __tablename__ = 'aircraft'

    id = db.Column(db.Integer, primary_key=True)
    icao24 = db.Column(db.String(8), unique=True, nullable=False, index=True)
    callsign = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    positions = db.relationship('PositionHistory', backref='aircraft',
                                lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'icao24': self.icao24,
            'callsign': self.callsign,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class PositionHistory(db.Model):
    __tablename__ = 'position_history'

    id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False, index=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Float)   # metres
    velocity = db.Column(db.Float)   # m/s
    heading = db.Column(db.Float)    # degrees
    vertical_rate = db.Column(db.Float)
    on_ground = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'velocity': self.velocity,
            'heading': self.heading,
            'vertical_rate': self.vertical_rate,
            'on_ground': self.on_ground,
            'timestamp': self.timestamp.isoformat(),
        }
