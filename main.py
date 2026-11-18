from datetime import datetime, timedelta
import logging
import os
from modules.extract_function import extract_func
from modules.unzip_function import unzip_func
from modules.load_function import load_func
from dotenv import load_dotenv

# ----- Set up logging 🪵-----
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

log_dir = 'logs' #Creating logs directory and filenames
os.makedirs(log_dir, exist_ok=True) 
log_filename = f'{log_dir}/{timestamp}.log' 

logging.basicConfig( #configuring logs
    filename=log_filename,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

logger = logging.getLogger() #assining logger to variable 
logger.info('Logger was successfully initialised.')

# ----- Defining variables 💬-----
zip_dir = 'zip'

url = 'https://analytics.eu.amplitude.com/api/2/export'

yesterday = datetime.now() - timedelta(days=1) #calculate yesterday

attempt = 1
max_attempts = 3

# ----- Retrieving API Keys 🔑-----
load_dotenv() 

API_KEY = os.environ.get("AMP_API_KEY") #retrieving passkeys from .env
SECRET_KEY = os.environ.get("AMP_SECRET_KEY")

# ----- Extracting -----
extract_result = extract_func(zip_dir, API_KEY, SECRET_KEY, url,yesterday)

if extract_result: #if the extraction was successful then do the following
    # ----- Defining variables for unzip -----
    data_dir = "data"
    zip_dir = 'zip'

    # ----- Unzipping -----
    unzip_result = unzip_func(data_dir, zip_dir, yesterday)

else:
    logger.info('No zip extracted, nothing to unzip. Unzip aborted.')

if unzip_result: #if unzipping was successful then do the following
    # ----- Retrieving AWS keys 🔑-----
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY') #directs to the env file and accessing the different variables
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    load_result = load_func(data_dir, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME)
else:
    logger.info('Unzip extracted no data, nothing to attempt to upload. Upload aborted.')