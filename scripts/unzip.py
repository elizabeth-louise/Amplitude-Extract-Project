import zipfile

try: #if unable to print contents of the zipfile then print the error
    with zipfile.ZipFile("zip/2026-11-12 12-18-34.zip") as file: 
        file.printdir()
except zipfile.BadZipFile as error: 
    print(error)