from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marsstatistics")


@app.route("/")
def home():

    mars_result=mongo.db.mars.find_one()
    print("mars_result " , mars_result)
    return render_template("index.html", mars=mars_result)


@app.route("/scrape")
def scrape():

    results=scrape_mars.scrape()
    mongo.db.mars.update({}, results, upsert=True)

    return redirect("/")

    
if __name__ == "__main__":
    app.run(debug=True)

