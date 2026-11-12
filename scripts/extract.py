import os
import json
import requests
import logging
import time
from datetime import datetime
from dotenv import load_dotenv
from zipfile import ZipFile 

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

log_dir = 'logs' #Creating logs directory and filenames
os.makedirs(log_dir, exist_ok=True) 
log_filename = f'{log_dir}/{timestamp}.log' 

logging.basicConfig( #configuring logs
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

logger = logging.getLogger() #assining logger to variable 
logger.info('Logger was successfully initialised.')

zip_dir = 'zip' #creating folder and file name for zip files
os.makedirs(zip_dir,exist_ok=True)
zipfilename = f'{zip_dir}/{timestamp}.zip'

data_dir = 'data' #create data folder and file name for jsons
os.makedirs(data_dir,exist_ok=True)
filename = f'{data_dir}/{timestamp}.json'

load_dotenv() 

API_KEY = os.environ.get("AMP_API_KEY") #retrieving passkeys from .env
SECRET_KEY = os.environ.get("AMP_SECRET_KEY")

url = 'https://analytics.eu.amplitude.com/api/2/export'

chosen_date = '20261111' #variable so can easily change the date of data being brought through

attempt = 1
max_attempts = 2

while attempt <= max_attempts:
    response = requests.get(
        url,
        params={
            "start": f'{chosen_date}T00', 
            "end": f'{chosen_date}T23'
            },
        auth=(API_KEY, SECRET_KEY)
    )
    status_code = response.status_code

    if status_code==200: #add more layers to the if statment
        with open(zipfilename,'wb') as output_file:
            output_file.write(response.content)
        print(f'File {zipfilename} saved successfully!🙂')
        logger.info(f'File {zipfilename} saved successfully!🙂')
        break
    else: #elif 300<= status_code <500:
        print(f'API call falied, status code {status_code} ☹️')
        logger.error(f'API call falied, status code {status_code} ☹️')
    
    attempt+=1 #increase the attempt variable
    time.sleep(30) #wait 30s before retrying
