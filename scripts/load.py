import os
import json
import logging
from datetime import datetime
import boto3 #library to connect with AWS
from dotenv import load_dotenv

# ----- Set Log filepath location -----
log_filename = f"logs/load_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# ----- Configure logs to retrieve INFO messages and higher -----
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

# ----- Retrieving keys 🔑 -----
load_dotenv() #access to .env file

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY') #directs to the env file and accessing the different variables
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# ----- Data file location 📁 -----
data_dir = 'data'
file_location = os.listdir(data_dir) #creates a list of everything in the data directory

# ----- Connecting to S3 🔗 -----
s3_client = boto3.client(
    's3', #what service we are trying to connect to
    aws_access_key_id = AWS_ACCESS_KEY, #this is case sensitive so don't mix the variables with what it is calling
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY #make sure lowercase to name the parameter 
)

# ----- Uploading file to bucket 🪣 -----
for file in file_location:
    to_upload = f'{data_dir}/{file}' #loops each file path for every file in the data directory
    try:
        s3_client.upload_file(to_upload, AWS_BUCKET_NAME, file) #file path, the output location in S3, name of the file in the bucket
        print(f'File {file} successfully uploaded!')
        logger.info(f'File {file} successfully uploaded!')
        os.remove(to_upload) #once uploaded, delete the file from the local save
    except Exception as e: #if something goes wrong with the upload
        print(f'Something went wrong. Error: {e}')
        logger.error(f'Something went wrong. Error: {e}')

# ----- What is already in the bucket? -----
def list_files_bucket(AWS_BUCKET_NAME): #creating function for listing files in a bucket
    response = s3_client.list_objects_v2( #list objects in the following bucket
        Bucket= AWS_BUCKET_NAME
    )
    list = response["Contents"] #response is a dictionary, retrieivng the contents
    for item in list:
        print(item["Key"]) #response is a list, retrieving the filename from the list