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


from models import Radiosonde

@app.route('/')
def index():
    param_wmoid = request.args.get('wmo_id')
    radiosonde = db.session.query(Radiosonde).filter_by(wmo_id=param_wmoid).order_by(desc(Radiosonde.sonde_validtime)).first()

    if radiosonde:
        return jsonify({
            'WMO_id': radiosonde.wmo_id,
            'id': radiosonde.id,
            'Sonde validtime': radiosonde.sonde_validtime.strftime("%Y-%m-%d %H:%M:%S"),
            'Updated at': radiosonde.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'Station Name': radiosonde.station_name,
            'latitude': radiosonde.lat,
            'longitude': radiosonde.lon,
            'PressurehPa': radiosonde.pressurehPA,
            'TemperatureK': radiosonde.temperatureK,
            'DewpointK': radiosonde.dewpointK,
            'u_windMS': radiosonde.u_windMS,
            'v_windMS': radiosonde.v_windMS
    })
    else:
        return jsonify({"Error": "No Entries found"})




if __name__ == '__main__':
    #app.debug = True
    app.run()
