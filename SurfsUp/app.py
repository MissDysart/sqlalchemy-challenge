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

# Declare some variables
# Calculate the year prior to given date of 2017-08-23
year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# List of agregates to select in queries for Dynamic Routes
sel = [func.min(Measurement.tobs),
       func.avg(Measurement.tobs),
       func.max(Measurement.tobs)]

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
        f"<br/>"
        f"Replace 'start' and 'end' with dates in yyyy-mm-dd format:<br/>"
        f"/api/v1.0/start/<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the results of the precipitation analysis for the last 12 months"""
    # year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).order_by(Measurement.date.desc()).all()
    
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
    
    # and JSON-ify!
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def observations():
    """Return the dates and temperature observations of the most-active station for the last 12 months"""
    # year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
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



@app.route("/api/v1.0/start")
def temps_user_start_to_last():
    """Return the minimum temperature, the average temperature,
    and the maximum temperature (>= start date) for a user-specified start date"""
    start_date = "2016-08-23"
    #start_date = dt.datetime.strftime(input(), "%Y-%m-%d")
    # sel = [func.min(Measurement.tobs),
    #        func.avg(Measurement.tobs),
    #        func.max(Measurement.tobs)]
    # temp_aggs = session.query(*sel).filter(Measurement.date >= start_date).all()
    # temp_info = list(np.ravel(temp_aggs))
    start_to_last_temp_aggs = list(np.ravel(session.query(*sel).filter(Measurement.date >= start_date).all()))
    #return jsonify(f"Min Temp: {temp_info[0]}, Average Temp: {temp_info[1]}, Max Temp: {temp_info[2]}")
    
    return jsonify(start_to_last_temp_aggs)

@app.route("/api/v1.0/start/end")
def temps_user_start_to_user_end():
    """Return the minimum temperature, the average temperature,
    and the maximum temperature for user-specified start-end range"""

    end_date = "2016-08-23"
    start_date = "2016-01-31"

    start_to_end_temp_aggs = list(np.ravel(session.query(*sel).\
                                        filter(Measurement.date >= start_date).\
                                        filter(Measurement.date <= end_date).all()))

    return jsonify(start_to_end_temp_aggs)

# Close the session
session.close()

# Define main behavior
if __name__ == '__main__':
    app.run(debug=True)