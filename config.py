import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    BASE_URL = os.getenv("BASE_URL")
    TIMEOUT = int(os.getenv("TIMEOUT"))