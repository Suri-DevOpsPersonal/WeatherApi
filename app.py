#! /usr/bin/env python3

from flask import Flask, render_template
from flask import jsonify, request
import asyncio
import os
# import aiohttps
from services.weather_service import get_multiple_weather
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html") 

@app.route("/get-city-weather")
def get_city_weather():
    city_input = request.args.get("city")
    if city_input:
        cities = [c.strip() for c in city_input.split(",")]
        weather_data = asyncio.run(get_multiple_weather(cities))
        city_count = len(weather_data)

        if request.args.get("format") == "json":
            return jsonify({
                "city_count": city_count,
                "data": weather_data
                })
        return render_template(
            "fetch-weather.html",
            weather_data=weather_data,
            city_count=city_count
            )
    
    return render_template("get-city-weather.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT",5000)),
                     debug=True
            )
