# Upload all downloaded SMARD files from my laptop (data/raw)
# into the Databricks volume energy.bronze.landing.
# Run from the project folder with (.venv) active:
#   python ingestion/upload_to_volume.py

import os                                     # to list the files in a folder

from databricks.sdk import WorkspaceClient    # ready-made tools to talk to Databricks
from dotenv import load_dotenv                # to read my .env file

VOLUME = "/Volumes/energy/bronze/landing"     # where the files go: /Volumes/catalog/schema/volume
RAW_FOLDER = "data/raw"                       # where the files are on my laptop

load_dotenv()            # reads .env → DATABRICKS_HOST and DATABRICKS_TOKEN
w = WorkspaceClient()    # logs in to Databricks with those two values

for name in os.listdir(RAW_FOLDER):                    # every file name in data/raw, e.g. 4169_1793574000000.json
    with open(f"{RAW_FOLDER}/{name}", "rb") as f:      # open the file as raw bytes ("rb" = read binary)
        # Send the file to the same name in the volume.
        # overwrite=True: same name → replace the old file, never a copy (daily mode re-downloads new weeks).
        w.files.upload(f"{VOLUME}/{name}", f, overwrite=True)
    print("uploaded", name)
