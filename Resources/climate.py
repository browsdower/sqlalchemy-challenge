from flask import Flask, render_template, redirect, jsonify

#dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import pandas as pd
import numpy as np
import datetime

app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurements
Stations = Base.classes.stations

session = Session(engine)

@app.route("/")
def home():
	print("Server received request for 'Home' page.")
	return "Hawaii Climate API"