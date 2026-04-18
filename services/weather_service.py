#! /usr/bin/env python3

import asyncio
import aiohttp
from datetime import datetime,timezone, timedelta

API_KEY = "9572426d283b012826622f6a5749f8b9"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather(city_name):
    """Featch weather for a city asyncronomously"""
    async with aiohttp.ClientSession() as session:
        params = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                main = data['main'] 
                weather = data['weather'][0]
                dt = datetime.fromtimestamp(data['dt'], tz=timezone(timedelta(seconds=data['timezone'])))
                current_dt = dt.strftime("%Y-%m-%d, Time: %I:%M:%S %p")
                return {"city": data['name'], "temperature": main['temp'], "description": weather['description'], "feels_like": main['feels_like'], "current_dt": current_dt}
            else:
                error_text = await response.text()
                return f"No City Found {city_name}. Error: {error_text}"

async def get_multiple_weather(cities):
    """Fetch weather for multiple cities asyncronomously"""
    tasks = [get_weather(city) for city in cities]
    return await asyncio.gather(*tasks)