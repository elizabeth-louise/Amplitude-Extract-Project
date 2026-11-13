# Amplitude-Extract-Project

A python-based data pipeline that extracts data from the Amplitude export API.


### extract.py 
* Creates directories for logging, zip files, and data files
* Retrieves API secret keys from .env file
* Creates API url and date variable
* Creates a **while** loop to send request to the API and
  * if successful save the zipfile
  * if unsuccesssful, depending on the status code either break the loop or continue until 3 attempts have been made
