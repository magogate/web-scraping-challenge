#https://stackoverflow.com/questions/31252791/flask-importerror-no-module-named-flask
#https://stackoverflow.com/questions/10572498/importerror-no-module-named-sqlalchemy
import pymongo
import scrape_mars
from flask import Flask, jsonify, render_template, flash

cliant = pymongo.MongoClient("mongodb://localhost:27017")

# https://stackoverflow.com/questions/28207761/where-does-flask-look-for-image-files
# https://stackoverflow.com/questions/22259847/application-not-picking-up-css-file-flask-python
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    db = cliant.mission_mangal
    #db.movies.find() is a cursor and you can not pass that to html page
    #so, we need to convert that to list    
    mars_info = list(db.mangal.find())    
    print(len(mars_info))
    # flash(mars_info)
    return render_template("index.html", marsInfo=mars_info)  


@app.route("/scrape")
def getMarsData():
    db = cliant.mission_mangal
    mars_info = list(db.mangal.find())
    mangal_info = scrape_mars.scrape()
    if len(mars_info) < 1:
        db.mangal.insert_one(mangal_info)
    else:
        # https://www.w3schools.com/python/python_mongodb_delete.asp
        db.mangal.delete_many({})
        db.mangal.insert_one(mangal_info)

    mars_info = list(db.mangal.find())
    return render_template("index.html", marsInfo=mars_info)


if __name__ == "__main__":
    app.run(debug=True)
