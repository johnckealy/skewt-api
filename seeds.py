from app import db
from datetime import datetime
from models import Radiosonde


def populate(sonde_validtime, wmo_id, station_name, lat, lon, temperatureK, dewpointK, pressurehPA, u_windMS, v_windMS):
    radiosonde = Radiosonde(sonde_validtime=sonde_validtime, wmo_id=wmo_id, station_name=station_name,
                            lat=lat, lon=lon, temperatureK=temperatureK, dewpointK=dewpointK,
                            pressurehPA=pressurehPA, u_windMS=u_windMS, v_windMS=v_windMS)
    db.session.add(radiosonde)
    db.session.commit()


db.session.query(Radiosonde).delete()


populate(sonde_validtime=datetime(2020, 3, 24, 12, 5), wmo_id="06544", station_name="Berlin",
         lat=23.3, lon=12.2, temperatureK=[300, 310, 312], dewpointK=[298, 278,288],
         pressurehPA=[1000, 950, 850], u_windMS=[2.3, 3.2, 1.2], v_windMS=[1.1, 2.3, 2.2])

populate(sonde_validtime=datetime(2020, 3, 24, 11, 18), wmo_id="06544", station_name="Berlin",
         lat=23.3, lon=12.2, temperatureK=[300, 310, 312], dewpointK=[298, 278,288],
         pressurehPA=[1000, 950, 850], u_windMS=[2.3, 3.2, 1.2], v_windMS=[1.1, 2.3, 2.2])

populate(sonde_validtime=datetime(2020, 3, 23, 6, 30), wmo_id="012343", station_name="Cork",
         lat=23.3, lon=12.2, temperatureK=[300, 310, 312], dewpointK=[298, 278,288],
         pressurehPA=[1000, 950, 850, 600], u_windMS=[2.3, 3.2, 1.2], v_windMS=[1.1, 2.3, 2.2])

populate(sonde_validtime=datetime(2020, 3, 24, 12, 15), wmo_id="05432", station_name="Sligo",
         lat=23.3, lon=12.2, temperatureK=[300, 310, 312], dewpointK=[298, 278,288],
         pressurehPA=[1000, 950, 850], u_windMS=[2.3, 3.2, 1.2], v_windMS=[1.1, 2.3, 2.2])

populate(sonde_validtime=datetime(2020, 3, 23, 23, 20), wmo_id="02344", station_name="Hawaii",
         lat=23.3, lon=12.2, temperatureK=[300, 310, 312], dewpointK=[298, 278,288],
         pressurehPA=[1000, 950, 850], u_windMS=[2.3, 3.2, 1.2], v_windMS=[1.1, 2.3, 2.2])
