import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#precipitation: df from jupyter notebook is already in correct format for jsonify
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_dict = prcp_df.to_dict()
    return jsonify(prcp_dict)

#stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all stations
    results = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


#tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all tobs in the last year
    tobs_list = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23')
    session.close()
    all_tobs = list(np.ravel(tobs_list))
    return jsonify(all_tobs)


#start
@app.route("/api/v1.0/<start>")
def start_date():
    #take an input date to show stats after
    input_date = input("Enter a date (yyyy-mm-dd).")
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all tobs after input date
    min_temp = session.query(Measurement.id, Measurement.station, func.min(Measurement.tobs)).filter(Measurement.date >= input_date).group_by(Measurement.id).order_by(func.min(Measurement.tobs)).first()
    max_temp = session.query(Measurement.id, Measurement.station, func.max(Measurement.tobs)).filter(Measurement.date >= input_date).group_by(Measurement.id).order_by(func.max(Measurement.tobs).desc()).first()
    avg_temp = session.query(Measurement.id, Measurement.station, func.avg(Measurement.tobs)).filter(Measurement.date >= input_date).group_by(Measurement.id).first()

    session.close()
    stats_start_list= [["TMIN", min_temp], ["TMAX", max_temp], ["TAVG", avg_temp]]
    all_start_stats = list(np.ravel(stats_start_list)
    return jsonify(all_start_stats)

#between
@app.route("/api/v1.0/<start>")
def between_dates():
    #take two start and end input dates
    start_date = input("Enter a start date (yyyy-mm-dd).")
    end_date = input("Enter an end date (yyyy-mm-dd).")
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all tobs after input date
    min1_temp = session.query(Measurement.id, Measurement.station, func.min(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.id).order_by(func.min(Measurement.tobs)).first()
    max1_temp = session.query(Measurement.id, Measurement.station, func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.id).order_by(func.max(Measurement.tobs).desc()).first()
    avg1_temp = session.query(Measurement.id, Measurement.station, func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.id).first()

    session.close()
    stats_between_list= [["TMIN", min1_temp], ["TMAX", max1_temp], ["TAVG", avg1_temp]]
    all_between_stats = list(np.ravel(stats_start_list)
    return jsonify(all_between_stats)

if __name__ == '__main__':
    app.run(debug=True)
