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

# List of aggregates to select in queries for dynamic routes
sel = [func.min(Measurement.tobs),
       func.avg(Measurement.tobs),
       func.max(Measurement.tobs)]

# Date format for dynamic route queries
date_format = func.strftime("%Y-%m-%d", Measurement.date)

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


# Dynamic Routes

@app.route("/api/v1.0/<start>")
def temps_user_start_to_last(start):
    """Return the minimum temperature, the average temperature,
    and the maximum temperature (>= start date) for a user-specified start date"""

    # Accept user input
    start_date = start.replace(" ", "")
    # Run query with user input
    if start_date >= "2010-01-01" and start_date < "2017-08-23":
        start_to_last_temp_aggs = list(np.ravel(session.query(*sel).\
                                        filter(date_format >= start_date).all()))
        # and JSON-ify!
        return jsonify(start_to_last_temp_aggs)
    # Print an error if the dates do not follow parameters
    return jsonify({"error": "Dates must follow the format of yyyy-mm-dd and fall bewteen 2010-01-01 and 2017-08-22."}), 404

@app.route("/api/v1.0/<start>/<end>")
def temps_user_start_to_user_end(start, end):
    """Return the minimum temperature, the average temperature,
    and the maximum temperature for user-specified start-end range"""
    # Accept user input
    start_date = start.replace(" ", "")
    end_date = end.replace(" ", "")
    # Run query with user input
    if start_date >= "2010-01-01" and end_date <= "2017-08-23":
        start_to_end_temp_aggs = list(np.ravel(session.query(*sel).\
                                        filter(date_format >= start_date).\
                                        filter(date_format <= end_date).all()))
        # and JSON-ify!
        return jsonify(start_to_end_temp_aggs)
    # Print an error if the dates do not follow parameters
    return jsonify({"error": "Dates must follow the format of yyyy-mm-dd and fall bewteen 2010-01-01 and 2017-08-23."}), 404
    

# Close the session
session.close()

# Define main behavior
if __name__ == '__main__':
    app.run(debug=True)