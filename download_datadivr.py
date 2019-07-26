import requests
import zipfile
import shutil
import os
import sys

username_password_path = os.path.join(os.getcwd(), "asimov_auth")
DATADIVR_PATH = os.path.realpath(os.path.join(os.path.dirname(os.getcwd()), "test.txt"))

try:
    with open(username_password_path, 'r') as file:
        lines = file.readlines()
        username = lines[0][:-1]
        print(username)
        password = lines[1][:-1]
        print(password)
except Exception as e:
    print("error occurred!")
    print(e)
    sys.exit()


url = 'http://asimov.westeurope.cloudapp.azure.com:8080/jen_test/myfile.txt'
filename = os.path.basename("test.txt")

r = requests.get(url, auth=(username,password))

with open(DATADIVR_PATH, 'wb') as file:
    for chunk in r.iter_content():
        file.write(chunk)
#response = requests.get(url)

#urllib.request.urlretrieve(url, filename)

#with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
#    zip_ref.extractall(directory_to_extract_to)
