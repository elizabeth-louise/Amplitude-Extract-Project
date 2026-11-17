# Amplitude-Extract-Project

A python-based data pipeline that extracts data from the Amplitude export API.

### What do you need to run this?

To access the Amplitude Extract API, you will need to have an API_KEY and SECRET_KEY.
You will also need to install the following libraries:

- requests
- python-dotenv

### Order of Excecution

1. extract.py
2. unzip.py
3. load.py

### API Documentation

See the Amplitude Export API documentation here. https://amplitude.com/docs/apis/analytics/export

Key things to note:

- If in the EU replace the default URL with 'https://analytics.eu.amplitude.com'
- Start and end time parameters are required (YYYYMMDDTHH)
- The Export API events are timestamped in UTC
- The size limit of the export is 6GB
- The rate limit is 4 concurrent requests and 360 requests per hour
- There is a 2 hour delay to events being available in the API

## Part One: Extract

I developed two python scripts to extract from the API. Firstly, I created the extract.py file which retrieves the initial response from the API. Then, as the response was a zip file, I created an unzip.py file to retrieve the .json files (after decompressing further .gzip files). See more detail on these below.

### Summary of python files

<details> 
<summary>extract.py</summary>

- Creates directories for logging, zip files, and data files
- Retrieves API secret keys from .env file
- Creates API url and dynamic date for parameters
- Creates a while loop to send request to the API and
_ if successful save the zipfile
_ if unsuccesssful, depending on the status code either break the loop or continue until 3 attempts have been made
</details>

<details> 
<summary>unzip.py</summary>

- Creates a temporary directory to save the gzips into
- Creates the name of the file to match the output of extract.py
- Extracts all the gzips from the zip into the temporary directory
- Creates a path for the gzip files
- Decompresses the gzips to save jsons into the data directory
- Closes the temporary directory and removes the original zip file
</details>
<br>
The data retrieved will always be for the whole day yesterday.

## Part Two: Load 

The aim of the load step was to upload the .json files into an S3 bucket and into Snowflake. There are a few steps required to set this up. See the image below for the concepts included in this:

<img src="assets\Load Plan.png" />

#### AWS

Firstly, I setup the requirements in AWS:

- Created the S3 bucket (with bucket versioning enabled)
- Created KMS (key management service) key
- Created the policy (what permissions do we have for the S3 bucket and encryption/decryption for KMS key)
-  Created user
Created role

#### Python

I then developed one python script which loads the data to an S3 bucket. This script uploads all files which are in the data folder to my S3 bucket. See the section below for further details.

#### Snowflake

Lastly, I set up the connection with Snowflake:

- Created a schema for the project
- Created the storage integration wth the bucket name and role ARN
- Created the trust relationship by connecting keys from Snowflake into the role in AWS
- Created a stage to see the data from the bucket
- Created an empty table and copied the .json files into it


### Summary of python file

<details> 
<summary>load.py</summary>

- Retrieves AWS keys from .env
- Locates the data files
- Connects to the S3 bucket
- Checks the files in the bucket against the files to upload and returns a list matches
- Two for loops that upload data files to the bucket
    - First loop uploads the matched files and returns a message that a new version has been uploaded
    - Second loop uploads any files that are left
</details>
