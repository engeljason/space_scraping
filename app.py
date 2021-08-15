import scraper
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#########################
## Flask App
#########################
app = Flask(__name__)


@app.route("/")
def page():
    return ""


if __name__ == '__main__':
    app.run()
