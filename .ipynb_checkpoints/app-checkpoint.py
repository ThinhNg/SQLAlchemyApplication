import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,desc,and_

from flask import Flask, jsonify

import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017-03-22<br/>"
        f"/api/v1.0/2017-03-22/2017-03-30 <br/>"
    )


@app.route("/api/v1.0/precipitation")
def Precipitation():
    # Query all dates and precipitation and creates a dict using the dates/precips.
    session = Session(engine)
    Result = session.query(Measurement.date,Measurement.prcp).all()
    DICT = {}
    for row in Result:
        DICT.update(dict([row]))
    session.close()

    return jsonify(DICT)


@app.route("/api/v1.0/stations")
def Stations():
    session = Session(engine)
    #Gets list of stations
    StationsList = session.query(Station.station).all()
    session.close()
    
    return jsonify(StationsList)



@app.route("/api/v1.0/tobs")
def Temperature():
    session = Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    DateMax = session.query(func.max(Measurement.date))
    LastDate = DateMax.scalar()
    LatestDate = dt.datetime.strptime(LastDate, '%Y-%m-%d')
    StartingDate = LatestDate -dt.timedelta(days=365)
    StartingDate=StartingDate.date()
    
    #Gets lists of date/temperatures.
    Result = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= StartingDate).all()
    session.close()
    return jsonify(Result)

@app.route("/api/v1.0/<start>")
def StartTempSummary(start):
    session = Session(engine)
    Result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    return jsonify(Result)

@app.route("/api/v1.0/<start>/<end>")
def StartEndTempSummary(start,end):
    session = Session(engine)
    Result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(Result)
#Reads in the start and end value and sorted them"






if __name__ == '__main__':
    app.run(debug=True)
