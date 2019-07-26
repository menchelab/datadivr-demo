import argparse
import os
import requests
import shutil
import sys
import zipfile

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--auth-file", required=True,
                help="Path to file containing authentication information.")
args = vars(ap.parse_args())

username_password_path = args["auth_file"]
DATADIVR_ZIP_PATH = os.path.realpath(os.path.join(os.path.dirname(os.getcwd()), "datadivr.zip"))
DATADIVR_PATH = os.path.realpath(os.path.join(os.path.dirname(os.getcwd())))

try:
    with open(username_password_path, 'r') as file:
        lines = file.readlines()
        username = lines[0][:-1]
        print(username)
        password = lines[1][:-1]
        print(password)
except Exception as e:
    print("An error occurred! Please make sure authentication file exists and is in this directory.")
    print(e)
    sys.exit()


url = 'http://asimov.westeurope.cloudapp.azure.com:8080/datadivr/DataDiVR.zip'
print("Downloading from ", url)

r = requests.get(url, auth=(username,password))
print("Download done! Writing zipfile to disk.")

with open(DATADIVR_ZIP_PATH, 'wb') as file:
    for chunk in r.iter_content():
        file.write(chunk)
print("File written! Unzipping and writing to %s." % DATADIVR_PATH)

with zipfile.ZipFile(DATADIVR_ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(DATADIVR_PATH)

os.remove(DATADIVR_ZIP_PATH)
