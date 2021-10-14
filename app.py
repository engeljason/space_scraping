import scraper
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask_pymongo import PyMongo

from flask import Flask, jsonify, render_template, redirect

#########################
## Flask App
#########################
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marsdb")

@app.route("/")
def page():
    mars_data = mongo.db.mars.find_one()
    if mars_data == None:
        return scrape()
    articles = mars_data['articles']
    mars_table = mars_data['table']
    mars_image = mars_data['mars_img']
    hemisphere_images = mars_data['hemispheres']
    
    return render_template('index.html', 
    articles = articles, 
    mars_table = mars_table, 
    mars_image = mars_image, 
    hemisphere_images = hemisphere_images)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraper.get_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)



if __name__ == '__main__':
    app.run()
