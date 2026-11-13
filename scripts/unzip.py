import os          
import zipfile     
import gzip        
import shutil     
import tempfile

# Create a temporary directory for extraction for all folder paths
temp_dir = tempfile.mkdtemp()

# Create local output directory for .json files to output to
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

#unpacks the zip folder to the temp directory, retrieves gzip files
with zipfile.ZipFile("zip/2026-11-12 12-18-34.zip", "r") as zip_ref: 
    zip_ref.extractall(temp_dir)

#finds all folders with numeric names and returns the file path as a variable
day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit()) #find the file path
day_path = os.path.join(temp_dir, day_folder) #variable for the file path

for root, _, files in os.walk(day_path): #os.walk traverses all subdirectories
    for file in files:
        if file.endswith('.gz'):
            # Process each .gz file
            print(file)

gz_path = os.path.join(root, file) #filepath of the .gz file
json_filename = file[:-3]  #filename of the .gz file and what it will be as a .json
output_path = os.path.join(data_dir, json_filename) #location to store the .json

with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file: #defining the gzip file path and output file path
    shutil.copyfileobj(gz_file, out_file) #command efficiently copies between file objects - copies the opening of the 

#delete the temporary directory
shutil.rmtree(temp_dir)

print("All files extracted to the 'data' directory!")
