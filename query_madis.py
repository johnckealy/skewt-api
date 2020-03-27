from app import db
from datetime import datetime
from models import Radiosonde


def populate(sonde_validtime, wmo_id, station_name, lat, lon, temperatureK, dewpointK, pressurehPA, u_windMS, v_windMS):
    radiosonde = Radiosonde(sonde_validtime=sonde_validtime, wmo_id=wmo_id, station_name=station_name,
                            lat=lat, lon=lon, temperatureK=temperatureK, dewpointK=dewpointK,
                            pressurehPA=pressurehPA, u_windMS=u_windMS, v_windMS=v_windMS)
    db.session.add(radiosonde)
    db.session.commit()

