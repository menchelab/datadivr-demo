import argparse
import os
import requests
import shutil
import sys
import zipfile
from distutils.dir_util import copy_tree


ap = argparse.ArgumentParser()
ap.add_argument("-a", "--auth-file", required=True,
                help="Path to file containing authentication information.")
args = vars(ap.parse_args())


username_password_path = args["auth_file"]

BIO_SELECTION_KEYWORDS = ["body", "cancer", "mental"]
DATADIVR_PATH = os.path.realpath(os.path.join(os.path.dirname(os.getcwd()), "DataDiVR"))

LAYOUTS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/layouts")
LINKS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/links")
LABELS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/labels")
SELECTIONS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/Selections")

TMP_ZIP_PATH = os.path.join(DATADIVR_PATH, "viveNet/Content/data/biodata.zip")
TMP_DATA_PATH = os.path.join(DATADIVR_PATH, "viveNet/Content/data/bio_layouts")
TMP_LAYOUTS_DIR = os.path.join(TMP_DATA_PATH, "layouts")
TMP_LINKS_DIR = os.path.join(TMP_DATA_PATH, "links")
TMP_LABELS_DIR = os.path.join(TMP_DATA_PATH, "labels")
TMP_SELECTIONS_DIR = os.path.join(TMP_DATA_PATH, "selections")



try:
    with open(username_password_path, 'r') as file:
        lines = file.readlines()
        username = lines[0][:-1]
        print("Connecting as ", username)
        password = lines[1][:-1]
except Exception as e:
    print("An error occurred! Please make sure authentication file exists and is in this directory.")
    print(e)
    sys.exit()


url = 'http://asimov.westeurope.cloudapp.azure.com:8080/datadivr/bio_layouts.zip'
print("Downloading from ", url)

r = requests.get(url, auth=(username,password))
print("Download done! Writing zipfile to disk.")

with open(TMP_ZIP_PATH, 'wb') as file:
    for chunk in r.iter_content():
        file.write(chunk)
print("File written! Unzipping and writing to %s." % TMP_DATA_PATH)

with zipfile.ZipFile(TMP_ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(os.path.dirname(TMP_DATA_PATH))

os.remove(TMP_ZIP_PATH)


new_layouts = [f for f in os.listdir(TMP_LAYOUTS_DIR) if
           os.path.isfile(os.path.join(TMP_LAYOUTS_DIR, f))]

layouts = [f for f in os.listdir(LAYOUTS_DIR) if
           os.path.isfile(os.path.join(LAYOUTS_DIR, f))] # and
           #any(f.startswith(x) for x in new_layouts)]

replaced_layouts = [l for l in new_layouts if any(l == ol for ol in layouts)]
replaced_layouts.sort()

print("\n\nLayouts (and corresponding links and labels) getting replaced: ", replaced_layouts)

existing_bio_selections = [f for f in os.listdir(SELECTIONS_DIR) if \
              os.path.isfile(os.path.join(SELECTIONS_DIR, f)) and \
              any(f.startswith(x) for x in BIO_SELECTION_KEYWORDS)]

new_selections = [f for f in os.listdir(TMP_SELECTIONS_DIR) if
           os.path.isfile(os.path.join(TMP_SELECTIONS_DIR, f))]

selections_to_remove = [f for f in existing_bio_selections if not f in new_selections]
if selections_to_remove:
    selections_to_remove.sort()
    print("\nSelections getting REMOVED: ", selections_to_remove)


selections_to_replace = [f for f in existing_bio_selections if f in new_selections]
if selections_to_replace:
    selections_to_replace.sort()
    print("\nSelections getting replaced: ", selections_to_replace)


while True:
     query = input('\nDo you want to continue? This cannot be undone! (yes/no)\n')
     Fl = query.lower().split()[0]
     if query == '' or not Fl in ['yes','no']:
        print('Please answer with yes or no! - you answered "%s"' % Fl)
     else:
        break
if Fl == 'no':
    sys.exit()

links_to_remove = [os.path.join(LINKS_DIR, f) for f in os.listdir(LINKS_DIR) if
               os.path.isfile(os.path.join(LINKS_DIR, f)) and
           any(f.startswith(x.split(".")[0]) for x in replaced_layouts)]
for links_list in links_to_remove:
    os.remove(os.path.join(LINKS_DIR, links_list))


labels_to_remove = [os.path.join(LABELS_DIR, f) for f in os.listdir(LABELS_DIR) if
               os.path.isfile(os.path.join(LABELS_DIR, f)) and
           any(f.startswith(x.split(".")[0]) for x in replaced_layouts)]
for labels_list in labels_to_remove:
    os.remove(os.path.join(LABELS_DIR, labels_list))

for selection in selections_to_remove:
    os.remove(os.path.join(SELECTIONS_DIR, selection))


# Copy the new layouts/links/labels/selections into their corresponding folders.
copy_tree(TMP_DATA_PATH, os.path.join(DATADIVR_PATH, "viveNet/Content/data"))

shutil.rmtree(TMP_DATA_PATH)
