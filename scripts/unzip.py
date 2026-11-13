# Define Logging
import logging
from datetime import datetime

# Set Log filepath location
log_filename = f"logs/unzip_folder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logs to retrieve INFO messages and higher
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

# Load libraries
import os
import zipfile
import gzip
import shutil
import tempfile
from datetime import datetime, timedelta

# Create a temporary directory for extraction for all folder paths
temp_dir = tempfile.mkdtemp()

# Create local output directory for .json files to output to
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
logger.info("Environment Setup: beginning unzip process")

zip_dir = 'zip'

yesterday = datetime.now() - timedelta(days=1) #calculate yesterday

start_time = yesterday.strftime('%Y%m%dT00') #format yesterday and 00:00

zipfilename = f'{zip_dir}/{start_time}-T23.zip'

try:
    # Extract the main zip file into the temporary directory - unpacks the zip folder to the temp directory, retrieves gzip files
    with zipfile.ZipFile(zipfilename, "r") as zip_ref: #
        zip_ref.extractall(temp_dir)
        logger.info(f"{zipfilename} extracted to temp directory: {temp_dir} ")
except Exception as e:
    logger.error(f"Error extracting zip file: {str(e)}")
    raise

try:
    # Locate the day folder (assumed to be the numeric folder) - finds all folders with numeric names and returns the file path as a variable
    day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit()) #find file paths with numeric names
    day_path = os.path.join(temp_dir, day_folder) #variable for the file path
except Exception as e:
    logger.error(f"Error finding day folder: {str(e)}")
    raise

# Walk through the day folder and decompress each .gz file to the data directory
for root, _, files in os.walk(day_path): #os.walk traverses all subdirectories
    for file in files:
        if file.endswith('.gz'): # Process each .gz file
            try:
                gz_path = os.path.join(root, file)  #filepath of the .gz file
                json_filename = file[:-3]  # Remove .gz extension
                output_path = os.path.join(data_dir, json_filename) #path for the output json file

                with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file: ##defining the gzip file path and output file path
                    shutil.copyfileobj(gz_file, out_file) ##command efficiently copies between file objects - copies the opening of the 
                
                logger.info(f"Successfully processed: {file} -> {json_filename}")
            except Exception as e:
                logger.error(f"Failed to process file {file}: {str(e)}")

try:
    # Delete the temporary directory
    shutil.rmtree(temp_dir)
    logger.info("Temp directory deleted")

except Exception as e:
    logger.error(f"Failed to delete temp directory: {str(e)}")

#remove the zip file after jsons have been extracted
try:
    os.remove(zipfilename)
    logger.info(f'zip file {zipfilename} deleted.')
except Exception as e:
    logger.error(f"Failed to delete zip file {zipfilename}: {str(e)}")

print("All files extracted to the 'data' directory!")

#may need to alter the file type to .jsonl if not working