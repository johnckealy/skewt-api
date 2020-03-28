from app import db
from datetime import datetime, timedelta
from faker import Faker
import random as rnd
from models import Radiosonde
from models import UpdateRecord



def populate(sonde_validtime, wmo_id, station_name, lat, lon, temperatureK, dewpointK, pressurehPA, u_windMS, v_windMS):
    radiosonde = Radiosonde(sonde_validtime=sonde_validtime, wmo_id=wmo_id, station_name=station_name,
                            lat=lat, lon=lon, temperatureK=temperatureK, dewpointK=dewpointK,
                            pressurehPA=pressurehPA, u_windMS=u_windMS, v_windMS=v_windMS)
    db.session.add(radiosonde)
    db.session.commit()


db.session.query(Radiosonde).delete()
db.session.query(UpdateRecord).delete()
fake = Faker()

for i in range(15):
    timestamp = datetime.utcnow()-timedelta(seconds=rnd.randint(1800,12000))
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    populate(sonde_validtime=timestamp,
             wmo_id=rnd.sample(["06544", "02349", "07653", "09583", "01234", "09834", "07642", "07654"], 1)[0],
             station_name=fake.city(), lat=23.3, lon=12.2, temperatureK=[300, 310, 312], dewpointK=[298, 278,288],
             pressurehPA=[1000, 950, 850], u_windMS=[2.3, 3.2, 1.2], v_windMS=[1.1, 2.3, 2.2])




record = UpdateRecord(updatetime=datetime.utcnow(), filename="test.gz")
db.session.add(record)
db.session.commit()
