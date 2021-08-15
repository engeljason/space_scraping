import scraper
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template



#########################
## Flask App
#########################
app = Flask(__name__)

@app.route("/")
def page():
    articles = scraper.get_articles()
    mars_table = scraper.get_mars_fact_table()
    mars_image = scraper.get_mars_image()
    hemisphere_images = scraper.get_mars_hemi_imgs()
    
    return render_template('index.html', 
    articles = articles, 
    mars_table = mars_table, 
    mars_image = mars_image, 
    hemisphere_images = hemisphere_images)


if __name__ == '__main__':
    app.run()
