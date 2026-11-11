# Upload the SMARD files that changed in the last 24 hours from my laptop (data/raw)
# into the Databricks volume energy.bronze.landing.
# Run from the project folder with (.venv) active, right AFTER the daily download:
#   python ingestion/upload_to_volume.py

import os                                     # to list the files in a folder and read their change time
import time                                   # to know the time right now

from databricks.sdk import WorkspaceClient    # ready-made tools to talk to Databricks
from dotenv import load_dotenv                # to read my .env file

VOLUME = "/Volumes/energy/bronze/landing"     # where the files go: /Volumes/catalog/schema/volume
RAW_FOLDER = "data/raw"                       # where the files are on my laptop
MAX_AGE = 24 * 60 * 60                        # 1 day in seconds (24 hours × 60 minutes × 60 seconds)

load_dotenv()            # reads .env → DATABRICKS_HOST and DATABRICKS_TOKEN
w = WorkspaceClient()    # logs in to Databricks with those two values

uploaded = 0             # counts how many files we upload

for name in os.listdir(RAW_FOLDER):                    # every file name in data/raw, e.g. 4169_1793574000000.json
    path = f"{RAW_FOLDER}/{name}"                      # full path: folder + file name
    age = time.time() - os.path.getmtime(path)         # now minus "last changed" = how old the file is, in seconds
    if age > MAX_AGE:                                  # not changed in the last 24 hours?
        continue                                       # → skip it, go to the next file (no upload)
    # Why skip old files? Every upload counts as a "changed file" for Auto Loader
    # (allowOverwrites), so uploading all files would load all of them into Bronze again.

    with open(path, "rb") as f:                        # open the file as raw bytes ("rb" = read binary)
        # Send the file to the same name in the volume.
        # overwrite=True: same name → replace the old file, never a copy (daily mode re-downloads new weeks).
        w.files.upload(f"{VOLUME}/{name}", f, overwrite=True)
    print("uploaded", name)
    uploaded += 1                                      # add 1 to the counter (short for uploaded = uploaded + 1)

print(f"done: {uploaded} files uploaded")              # no indent → runs once, after the loop
