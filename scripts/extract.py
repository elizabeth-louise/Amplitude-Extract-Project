import os
import json
import requests
import logging
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

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

yesterday = datetime.now() - timedelta(days=1) #calculate yesterday

start_time = yesterday.strftime('%Y%m%dT00') #format yesterday and 00:00
end_time = yesterday.strftime('%Y%m%dT23') #format yesterday and 23:00

# chosen_date = '20261111' #variable so can easily change the date of data being brought through, but also limited to one day so don't overload

attempt = 1
max_attempts = 3

while attempt <= max_attempts:
    response = requests.get(
        url,
        params={
            "start": {start_time}, 
            "end": {end_time}
            },
        auth=(API_KEY, SECRET_KEY)
    )
    status_code = response.status_code

    if status_code==200:
        try:
            with open(zipfilename,'wb') as output_file:
                output_file.write(response.content)
            print(f'File {zipfilename} saved successfully!🙂')
            logger.info(f'File {zipfilename} saved successfully!🙂')
            break
        except Exception as e:
            print(f'An error occurred when saving the zip file: {e}')
            logger.error(f'An error occurred when saving the zip file: {e}')
    elif 400<= status_code <500: #if the status code is in the 400s then check for specific codes and their meanings
        if status_code == 400:
            print('Check parameters: missing, invalid format, or exceed 6GB limit')
            logger.error('Check parameters: missing, invalid format, or exceed 6GB limit')
            break
        elif status_code == 401:
            print('Basic authentication header missing/malformed')
            logger.error('Basic authentication header missing/malformed')
            break
        elif status_code == 403:
            print('API or secret key is invalid or been blocked by Amplitude, check credentials and project region')
            logger.error('API or secret key is invalid or been blocked by Amplitude')
            break
        elif status_code == 404:
            print('No export files exist for the requested range')
            logger.error('No export files exist for the requested range')
            break
        elif status_code == 429:
            print('Request exceeds a rate or concurrency limit. Note: immediate retry doesn\'t resolve exhausted hourly budget')
            logger.error('Request exceeds a rate or concurrency limit')
            break
        else: #in case error code not listed above
            print('Failed, status code {status_code}. Investigate further')
            logger.error('Failed, status code {status_code}. Investigate further')
            break
    elif status_code == 504:
        print('Export timed out, retry with smaller range')
        logger.error('Export timed out, retry with smaller range')
        break
    else: 
        if attempt == max_attempts:
            print(f'Max number of attempts reached. Status code {status_code}. Investigate further 🔍')
            logger.warning(f'Max number of attempts reached. Status code {status_code}. Investigate further 🔍')
        else:
            print(f'Attempt {attempt} failed, status code {status_code}. Trying again 😅')
            logger.error(f'Attempt {attempt} failed, status code {status_code}. Trying again 😅')
    
    attempt+=1 #increase the attempt variable
    time.sleep(60) #wait 60s before retrying
