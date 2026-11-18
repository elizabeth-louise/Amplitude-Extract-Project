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

# ----- What is already in the bucket? 🔍-----
# def compare_files_bucket(AWS_BUCKET_NAME): #creating function for listing files in a bucket
response = s3_client.list_objects_v2( #list objects in the following bucket
    Bucket= AWS_BUCKET_NAME
)

s3_items=[] #declaring the list

item_list = response["Contents"] #response is a dictionary, retrieivng the contents
for item in item_list:
    s3_items.append(item["Key"]) #item is a list of dictionaries, retrieving the filename from the list (for each dictionary, retrieve the key) and adding to list of items

common_elements = set(s3_items).intersection(set(file_location)) #creating sets as allows to compare more easily, intersection compares the values and returns values that are the same

matched_items = []

# print(f"Common Elements: ")
for item in (common_elements): #for each item in the set print the value
    # print(item or "No common elements")
    matched_items.append(item)

# ----- Uploading to S3 Bucket 🪣 -----
for file in matched_items:
    to_upload = f'{data_dir}/{file}' #loops each file path for every file in the matched items
    try:
        s3_client.upload_file(to_upload, AWS_BUCKET_NAME, file) #file path, the output location in S3, name of the file in the bucket
        print(f'New version of file {file} successfully uploaded.\n See the versioning in the bucket to rollback any changes.')
        logger.info(f'New version of file {file} successfully uploaded. See the versioning in the bucket to rollback any changes.')
        os.remove(to_upload) #once uploaded, delete the file from the local save
    except Exception as e: #if something goes wrong with the upload
        print(f'Something went wrong. Error: {e}')
        logger.error(f'Something went wrong. Error: {e}')

file_location = os.listdir(data_dir) #updating the list as some files may have been deleted

for file in file_location:
    to_upload = f'{data_dir}/{file}' #loops each file path for every file (that is now left) in the data directory
    try:
        s3_client.upload_file(to_upload, AWS_BUCKET_NAME, file) #file path, the output location in S3, name of the file in the bucket
        print(f'File {file} successfully uploaded!')
        logger.info(f'File {file} successfully uploaded!')
        os.remove(to_upload) #once uploaded, delete the file from the local save
    except Exception as e: #if something goes wrong with the upload
        print(f'Something went wrong. Error: {e}')
        logger.error(f'Something went wrong. Error: {e}')
