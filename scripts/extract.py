import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from zipfile import ZipFile 

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

zip_dir = 'zip'
os.makedirs(zip_dir,exist_ok=True)
zipfilename = f'{zip_dir}/{timestamp}.zip'

data_dir = 'data'
os.makedirs(data_dir,exist_ok=True)
filename = f'{data_dir}/{timestamp}.json'

load_dotenv()

API_KEY = os.environ.get("AMP_API_KEY")
SECRET_KEY = os.environ.get("AMP_SECRET_KEY")

url = 'https://analytics.eu.amplitude.com/api/2/export'

response = requests.get(
    url,
    params={"start": "20261111T00", "end": "20261111T23"},
    auth=(API_KEY, SECRET_KEY)
)

status_code = response.status_code

if status_code==200:
    with open(zipfilename,'wb') as output_file:
        output_file.write(response.content)
    print(f'zip file {zipfilename} saved successfully!')
elif 300<= status_code <500:
        print(f'API call falied, status code {status_code} ☹️')
