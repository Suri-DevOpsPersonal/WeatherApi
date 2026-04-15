#! /usr/bin/env python3

import asyncio
import aiohttp

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
                print(f"City: {data['name']}")
                print(f"Temparature: {main['temp']}°C)")
                print(f"Description: {weather['description']}")
            else:
                error_text = await response.text()
                print(f"[{response.status}] Error for {city_name}: {error_text}")

async def main():
    
    cities = ["London", "Chennai", "Moscow", "New York"]
    tasks = [get_weather(city) for city in cities]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
