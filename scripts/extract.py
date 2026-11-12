import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("AMP_API_KEY")
SECRET_KEY = os.environ.get("AMP_SECRET_KEY")

# DATABASE_PASSWORD = os.environ.get("")

# print(SECRET_KEY)


url = 'https://analytics.eu.amplitude.com/api/2/export' #?start=&lt;starttime&gt;&end=&lt;endtime

response = requests.get(
    url,
    params={"start": "20261111T00", "end": "20261111T23"},
    auth=(API_KEY, SECRET_KEY)
)

status_code = response.status_code

print(status_code)