# SkewT API

*A Flask REST API providing data from the upper atmosphere in near-real time.*

This API is live at `api.skewt.org`.

You can query the radiosonde (weather balloon) data from any meteorological station if you know the station's identification number. A list of station details is included in the repository (or simple use the `available` route).

#### Usage Examples

Get the station data from Castor Bay, Northern Ireland

`https://api.skewt.org?wmo_id=0318`

Find the ID of the closest station to (-8.542, 54.299)

`https://api.skewt.org/nearest?lat=54.299&lon=-8.542`

Show the latitude, longitude, and WMO ID of all available radiosondes

`https://api.skewt.org/available` 


#### Installation

To initialize the database, you must run

```
$ python
>> from app import db
>> db.create_all()
>> from models import Station
>> Station.initialize_stations()
```

A cron job is required to keep the data flowing in. Run this script in the cron job.

`python query_madis.py`
