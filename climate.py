from flask import Flask, jsonify

#dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import pandas as pd
import numpy as np
import datetime

from climate_starter.ipynb import *

app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

Base.classes.keys()

session = Session(engine)

@app.route("/")
def home():
	# print("Server received request for 'Home' page.")
	"Hawaii Climate API"
	return (
		f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/<start>"
		f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date <= "2016-08-23", Measurement.date >= "2017-08-23").\
        all()

    precip_list = [results]

    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return the json list of all stations in the data set"""
    all_stations = session.query(Station.station, Station.name).all()
              
    stations_data = []
    for rec in range(len(all_stations)):
        station_dict = {}
        station_dict['station_id'] = all_stations[rec][0]
        station_dict['name'] = all_stations[rec][1]
        stations_data.append(station_dict)
    
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    recent_tobs = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
               filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
               group_by(Measurement.date).order_by(Measurement.date).all()

   
    tobs_data = []
    for rec in range(len(recent_tobs)):
        tobs_dict = {}
        tobs_dict['date'] = recent_tobs[rec][0]
        tobs_dict['temp'] = recent_tobs[rec][2]
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def temp_range(start):
    min_temp = session.query(func.min(Measurement.tobs)).\
               filter(Measurement.date == start).first()
    avg_temp = session.query(func.avg(Measurement.tobs)).\
               filter(Measurement.date == start).first()
    max_temp = session.query(func.max(Measurement.tobs)).\
               filter(Measurement.date == start).first()

    temp_data = [min_temp, avg_temp, max_temp]
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end_date>")
def temp_ranges(start, end_date):
    
    min_temp = session.query(func.min(Measurement.tobs)).\
               filter(Measurement.date.between(start, end_date)).first()
    avg_temp = session.query(func.avg(Measurement.tobs)).\
               filter(Measurement.date.between(start, end_date)).first()
    max_temp = session.query(func.max(Measurement.tobs)).\
               filter(Measurement.date.between(start, end_date)).first()
    
    date_data = [min_temp, avg_temp, max_temp]
    return jsonify(date_data)


if __name__ == '__main__':
    app.run(debug=True)
