# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """All available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the results of the precipitation analysis for the last 12 months"""
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).order_by(Measurement.date.desc()).all()
    # session.close()
    # Convert to dictionary
    past_year_prcp = []
    for date, prcp in year_prcp:
        prcp_dict = {}
        prcp_dict[date] = prcp
        past_year_prcp.append(prcp_dict)
    # and JSON-ify!
    return jsonify(past_year_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    stations = session.query(Station.station).all()
    station_list = list(np.ravel(stations))
    # stations = session.query(Station.station, Station.name,
    #        Station.longitude, Station.latitude,
    #        Station.elevation).order_by(Station.station).all()
    # station_list = []
    # for station, name, longitude, latitude, elevation in stations:
    #     station_dict = {}
    #     station_dict["Station"] = station
    #     station_dict["Name"] = name
    #     station_dict["Longitude"] = longitude
    #     station_dict["Latitude"] = latitude
    #     station_dict["Elevation"] = elevation
    #     station_list.append(station_dict)

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def observations():
    """Return the dates and temperature observations of the most-active station for the last 12 months"""
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_tobs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').filter(Measurement.date >= year_ago).\
        order_by(Measurement.date.desc()).all()

    # Convert to dictionary
    past_year_temp = []
    for date, temp in year_tobs:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature"] = temp
        past_year_temp.append(tobs_dict)
    # and JSON-ify!
    return jsonify(past_year_temp)


session.close()

if __name__ == '__main__':
    app.run(debug=True)