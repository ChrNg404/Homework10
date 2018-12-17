import numpy as np

from sqlalchemy import create_engine, Integer, MetaData, Table, Column
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

Base = automap_base()

Base.prepare(engine, reflect=True)

# produce our own MetaData object
metadata = MetaData()

metadata.reflect(engine)

print(metadata.tables.keys())

##Table('measurement', metadata,
#                Column('id', Integer, primary_key=True)
#           )

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#Flask setup
app=Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/precipitation"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation values"""
    #Query precipitation
    results = session.query(Measurement).all()
    
    #Create a dictionary and append everything into it
    precip_dict = []
    for measurement in results:
        precipitation_dict = {}
        precipitation_dict["date"] = measurement.date
        precipitation_dict["amount of rain"]= measurement.prcp
        precip_dict.append(precipitation_dict)
     
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")

def stations():
    """Return a list of stations"""
    results=session.query(Station).all()
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)       

@app.route("/api.v1.0/tobs")
def tobs():
    """Return dates and temperature observations from a year from the last date point"""
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2016-12-31').\
    order_by(Measurement.prcp).all()
    
    year_tobs = list(np.ravel(results))
    
    return jsonify(year_tobs)
   
#id INTEGER
#station TEXT
#date TEXT
#prcp FLOAT
#tobs FLOAT

if __name__=='__main__':
    app.run(debug=True)