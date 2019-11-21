#https://stackoverflow.com/questions/31252791/flask-importerror-no-module-named-flask
#https://stackoverflow.com/questions/10572498/importerror-no-module-named-sqlalchemy
import pymongo
import scrape_mars
from flask import Flask, jsonify, render_template, flash

cliant = pymongo.MongoClient("mongodb://localhost:27017")

# https://stackoverflow.com/questions/35309042/python-how-to-set-global-variables-in-flask
app = Flask(__name__)

@app.route("/")
def index():
    db = cliant.mission_mangal
    #db.movies.find() is a cursor and you can not pass that to html page
    #so, we need to convert that to list
    mars_info = list(db.mangal.find())    
    # flash(mars_info)
    return render_template("index.html", marsInfo=mars_info)  


@app.route("/scrape")
def getMarsData():
    db = cliant.mission_mangal
    mangal_info = scrape_mars.scrape()
    db.mangal.insert_one(mangal_info)    
    return mangal_info


if __name__ == "__main__":
    app.run(debug=True)