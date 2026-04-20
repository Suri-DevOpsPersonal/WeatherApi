#! /usr/bin/env python3

import asyncio
import aiohttp
from datetime import datetime, timezone, timedelta
from exceptions.exceptions import CityNotFoundError, WeatherServiceError, ExternalAPIError

API_KEY = "9572426d283b012826622f6a5749f8b9"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_weather(city_name):
    """Featch weather for a city asyncronomously"""
    async with aiohttp.ClientSession() as session:
        params = {"q": city_name, "appid": API_KEY, "units": "metric"}
        try:
            async with session.get(BASE_URL, params=params) as response:
                if response.status == 404:
                    raise CityNotFoundError(f"City not found: {city_name}")
                if response.status != 200:
                    raise ExternalAPIError(f"API Error: {response.status}")
                data = await response.json()
                main = data["main"]
                weather = data["weather"][0]
                current_dt = datetime.fromtimestamp(
                    data["dt"], tz=timezone(timedelta(seconds=data["timezone"]))
                )

                return {
                    "city": data["name"],
                    "temperature": main["temp"],
                    "description": weather["description"],
                    "feels_like": main["feels_like"],
                    "current_dt": current_dt
                }
        except aiohttp.ClientError as e:
            raise ExternalAPIError(f"Network error occurred: {str(e)}")

async def get_multiple_weather(cities):
    """Fetch weather for multiple cities asyncronomously"""
    tasks = [get_weather(city) for city in cities]
    return await asyncio.gather(*tasks, return_exceptions=True)
