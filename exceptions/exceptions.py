#! /usr/bin/env python3

class WeatherServiceError(Exception):
    pass

class CityNotFoundError(WeatherServiceError):
    pass

class ExternalAPIError(WeatherServiceError):
    pass
