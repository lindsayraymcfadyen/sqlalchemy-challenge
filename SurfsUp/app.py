# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine,reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(bind=engine)

#################################################
# Flask Setup
app = Flask(__name__)
#################################################
#################################################

## Flask Routes

#Home Route 
@app.route("/")
def home():
     """List all available api routes"""
     return (
          f"Available API Routes:  <br/>"
          f"Precipitation:  /api/v1.0/precipitation<br/>"
          f"Stations:  /api/v1.0/stations<br/>"
          f"Temperature (12 Months):  /api/v1.0/tobs<br/>"
          f"Temperature Stats (2016-08-23):  /api/v1.0/2016-08-23<br/>"
          f"Temperature Stats (2016-08-23 to 2017-8-23)  :/api/v1.0/2016-08-23/2017-08-23<br/>"
        )  


#Precipitation Route 
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return last 12 months of precipitation data"""
    #Precipitation Sesson 
    session = Session(engine)
    #Precipitaton Query 
    results = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        order_by(Measurement.date).all()
    session.close()
    #Precipitation Dictionary
    all_prcp = []
    for date, prcp in results:
        prcp_dictionary = {}
        prcp_dictionary["date"] = date
        prcp_dictionary["prcp"] = prcp
        all_prcp.append(prcp_dictionary)
    return jsonify(all_prcp)



#Station Route 
@app.route("/api/v1.0/stations")
def stations():
    """Return JSON list of stations """
    #Station Session 
    session = Session(engine)
    #Station Query 
    results = session.query(Station.station).all()
    session.close()
    #Convert list of tuples into normal list 
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)



#Tobs Route 
@app.route("/api/v1.0/tobs")
def tobs():
    """Return JSON list of temperature observations of most active station from last 12 months"""
    #Tobs Session 
    session = Session(engine)
    #Tobs Query 
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()
    session.close()
    #Tobs Dictionary 
    all_tobs = []
    for prcp, date, tobs in results:
        tobs_dictionary = {}
        tobs_dictionary["prcp"] = prcp
        tobs_dictionary["date"] = date
        tobs_dictionary["tobs"] = tobs
        all_tobs.append(tobs_dictionary)
    return jsonify(all_tobs)



#Start Route
@app.route("/api/v1.0/<start>")
def start_route(start):
    """Return JSON list of the minimum temperature, the average temperature, and the maximum temperature for 2016-08-23"""
    start= dt.datetime.strptime(start,'%Y-%m-%d')
    #Start Session 
    session = Session(engine)
    #Start Query 
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    #Start Dictionary 
    all_start = []
    for min, avg, max in results:
        start_dictionary =  {}
        start_dictionary["min_temp"] = min
        start_dictionary["avg_temp"] = avg
        start_dictionary["max_temp"] = max 
        all_start.append(start_dictionary)
    return jsonify(all_start)



#Start-End Route 
@app.route("/api/v1.0/<start>/<end>")
def start_end_route(start,end):
    """Return JSON list of the minimum temperature, the average temperature, and the maximum temperature from 2016-08-23 through 2017-08-23 """
    start = dt.datetime.strptime(start,'%Y-%m-%d')
    end = dt.datetime.strptime(end,'%Y-%m-%d')
    #Start-End Session
    session = Session(engine)
    #Start-End Query
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date>=start).filter(Measurement.date <= end).all()
    session.close()
    #Start_End Dictionary 
    all_start_end = []
    for min, avg, max in results:
        start_end_dictionary = {}
        start_end_dictionary["min_temp"] = min
        start_end_dictionary["avg_temp"] = avg
        start_end_dictionary["max_temp"] = max 
        all_start_end.append(start_end_dictionary)
    return jsonify(all_start_end)


if __name__ == "__main__":
    app.run(debug = True)




#################################################
