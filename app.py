#! /usr/bin/env python3

from flask import Flask, render_template
from flask import jsonify, request
import asyncio
import os
from services.weather_service import get_multiple_weather
from utils.logger import setup_logger

logger = setup_logger()
logger.info("Application started")
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html") 

@app.route("/get-city-weather")
def get_city_weather():
    json_data = []
    city_input = request.args.get("city")
    logger.info(f"Received request for city: {city_input}")
    if city_input:
        cities = [c.strip() for c in city_input.split(",")]
        weather_data = asyncio.run(get_multiple_weather(cities))
        city_count = len(weather_data)
        successful_cities = []        
        failed_cities = []
        for city, result in zip(cities, weather_data):
            if isinstance(result, Exception):
                logger.error(f"Error fetching weather for {city}: {str(result)}")
                failed_cities.append({
                    "city": city,
                    "error": str(result)
                    })
            else:
                logger.info(f"Successfully fetched weather for {city}")
                successful_cities.append(result)

        if request.args.get("format") == "json":
            for city in successful_cities:
                json_data.append({
                    **city,
                    "current_dt": city["current_dt"].isoformat()
                    })
            status_code = 200 if not failed_cities else 207
            return jsonify({
                "city_count": len(json_data),
                "scuccess_count": len(json_data),
                "error_count": len(failed_cities),
                "data": successful_cities,
                "errors": failed_cities
                }), status_code
        return render_template(
            "fetch-weather.html",
            successful_cities=successful_cities,
            failed_cities=failed_cities,
            city_count=city_count
            )
    
    return render_template("get-city-weather.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT",5000)),
                     debug=True
            )
