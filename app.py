from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import os
import random
from datetime import datetime, timedelta
from sqlalchemy import desc


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



if os.uname()[1] == 'leno':
    from dotenv import load_dotenv
    load_dotenv()
    POSTGRES = {
        'user': os.environ['PG_USER'],
        'pw': os.environ['PG_PWD'],
        'db': os.environ['PG_DATABASE'],
        'host': 'localhost',
        'port': '5432',
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jokea:mask9shop@localhost:5432/tephigrams-api-db'


heroku = Heroku(app)
db = SQLAlchemy(app)


from models import Radiosonde, Haversine

@app.route('/')
def index():
    param_wmoid = request.args.get('wmo_id')
    radiosonde = db.session.query(Radiosonde).filter_by(wmo_id=param_wmoid).order_by(desc(Radiosonde.sonde_validtime)).first()

    if radiosonde:
        return jsonify({
            "wmoId": radiosonde.wmo_id,
            "id": radiosonde.id,
            "sondeValidtime": radiosonde.sonde_validtime.strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": radiosonde.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "stationName": radiosonde.station_name,
            "latitude": radiosonde.lat,
            "longitude": radiosonde.lon,
            "pressurehPa": radiosonde.pressurehPA,
            "temperatureK": radiosonde.temperatureK,
            "dewpointK": radiosonde.dewpointK,
            "uWindMS": radiosonde.u_windMS,
            "vWindMS": radiosonde.v_windMS
        })
    else:
        return jsonify({"Error": "No Entries found"})



@app.route('/available')
def available():
    results = db.session.query(Radiosonde).filter(Radiosonde.sonde_validtime > datetime.utcnow()-timedelta(days=1))
    # available_sonde_wmoids = [i.sonde_validtime for i in available_sondes]
    available_sondes = []
    if results:
        for sonde in results:
            sonde_obj = {
               "wmoId": sonde.wmo_id,
               "lat": sonde.lat,
               "lon": sonde.lon
            }
            available_sondes.append(sonde_obj)

        return jsonify(available_sondes)
    else:
        return jsonify({"Error": "No available sondes found"})


@app.route('/nearest')
def nearest():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    available = db.session.query(Radiosonde).filter(Radiosonde.sonde_validtime > datetime.utcnow()-timedelta(days=1))

    v = {'lat': lat, 'lon': lon}
    nearest = Haversine.closest(available, v)

    return jsonify({ "wmoId": nearest.wmo_id })



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response


if __name__ == '__main__':
    #app.debug = True
    app.run()
