import os
import json
import requests
import logging
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def extract_func(zip_dir: str, API_KEY: str, SECRET_KEY: str, url: str, date: str):
    """Function to extract zip files from an API.

    Args:
        zip_dir (str): The name of the directory to save the zip files in
        API_KEY (str): The API key to access the API (use load_dotenv() to retrieve from .env file)
        SECRET_KEY (str): The secret key to access the API (use load_dotenv() to retrieve from .env file)
        url (str): The endpoint of the API
        date (str): The date to extract data for (in the format '%Y%m%d')

    Returns:
        boolean: returns true if the extraction was successful
    """

    start_time = date.strftime('%Y%m%dT00') #format yesterday and 00:00
    end_time = date.strftime('%Y%m%dT23') #format yesterday and 23:00

    os.makedirs(zip_dir,exist_ok=True)
    zipfilename = f'{zip_dir}/{start_time}-T23.zip'

    load_dotenv() 

    API_KEY = os.environ.get("AMP_API_KEY") #retrieving passkeys from .env
    SECRET_KEY = os.environ.get("AMP_SECRET_KEY")

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

                return True
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

    return False
