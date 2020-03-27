from app import db
from datetime import datetime

class Radiosonde(db.Model):
    __tablename__ = 'radiosondes'
    id = db.Column(db.Integer, primary_key=True)
    sonde_validtime = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    wmo_id = db.Column(db.String())
    station_name = db.Column(db.String())
    lat = db.Column(db.Float())
    lon = db.Column(db.Float())
    temperatureK = db.Column(db.ARRAY(db.Float))
    dewpointK = db.Column(db.ARRAY(db.Float))
    pressurehPA = db.Column(db.ARRAY(db.Integer))
    u_windMS = db.Column(db.ARRAY(db.Float))
    v_windMS = db.Column(db.ARRAY(db.Float))

    def __init__(self, sonde_validtime=None, wmo_id=None, station_name=None, lat=None, lon=None,
                 temperatureK=None, dewpointK=None, pressurehPA=None, u_windMS=None, v_windMS=None):
        self.sonde_validtime = sonde_validtime
        self.updated_at = datetime.utcnow()
        self.wmo_id = wmo_id
        self.station_name = station_name
        self.lat = lat
        self.lon = lon
        self.temperatureK = temperatureK
        self.dewpointK = dewpointK
        self.pressurehPA = pressurehPA
        self.u_windMS = u_windMS
        self.v_windMS = v_windMS



