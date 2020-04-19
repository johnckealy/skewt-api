from app import db
from datetime import datetime, timedelta
import csv
import re


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
        self.updated_at = datetime.utcnow()#.strftime("%Y-%m-%d %H:%M:%S")
        self.wmo_id = wmo_id
        self.station_name = station_name
        self.lat = lat
        self.lon = lon
        self.temperatureK = temperatureK
        self.dewpointK = dewpointK
        self.pressurehPA = pressurehPA
        self.u_windMS = u_windMS
        self.v_windMS = v_windMS



class UpdateRecord(db.Model):
    __tablename__ = 'update_times'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    updatetime = db.Column(db.DateTime())

    def __init__(self, filename=None, updatetime=None):
        self.filename = filename
        self.updatetime = updatetime#.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def delete_expired(cls, expiration_days):
        limit = datetime.now() - timedelta(days=expiration_days)
        cls.query.filter(cls.updatetime <= limit).delete()
        db.session.commit()



class Station(db.Model):
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)
    stn_wmoid = db.Column(db.String())
    stn_name = db.Column(db.String())
    stn_lat = db.Column(db.Float())
    stn_lon = db.Column(db.Float())
    stn_altitude = db.Column(db.Float())

    def __init__(self, stn_wmoid, stn_lat, stn_lon, stn_name, stn_altitude):
        self.stn_wmoid = stn_wmoid
        self.stn_lat = stn_lat
        self.stn_lon = stn_lon
        self.stn_name = stn_name
        self.stn_altitude = stn_altitude

    @classmethod
    def initialize_stations(cls):
        US_STATES = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID",
                     "IL", "IN", "KS","LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC",
                     "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD",
                     "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

        with open('station_list.txt', 'r') as csvfile:
            print("Running station initializer...")
            stndata = csv.reader(csvfile, delimiter='\t')
            for row in stndata:
                m = re.match(r"(?P<stn_wmoid>^\w+)\s+(?P<stn_lat>\S+)\s+(?P<stn_lon>\S+)\s+(?P<stn_altitude>\S+)(?P<stn_name>\D+)" , row[0])
                fields = m.groupdict()
                stn_wmoid = fields['stn_wmoid'][6:]
                stn_name = fields['stn_name'].strip()
                # import code; code.interact(local=dict(globals(), **locals()))

                if re.match(r"^[a-zA-Z]{2}\s", stn_name) and  stn_name[:2] in US_STATES:
                    stn_name = stn_name[2:].strip().title() + ", " + stn_name[:2]
                else:
                    stn_name = stn_name.title()
                stn_name = fields['stn_name'].strip().title()
                stn_lat = float(fields['stn_lat'])
                stn_lon = float(fields['stn_lon'])
                stn_altitude = float(fields['stn_altitude'])

                if stn_altitude != -998.8:
                    station = Station(stn_wmoid, stn_lat, stn_lon, stn_name, stn_altitude)
                    db.session.add(station)
                    db.session.commit()
