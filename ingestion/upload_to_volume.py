import os

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

VOLUME = "/Volumes/energy/bronze/landing"
RAW_FOLDER = "data/raw"

load_dotenv()            # reads .env → DATABRICKS_HOST and DATABRICKS_TOKEN
w = WorkspaceClient()    # logs in to Databricks with those two values

for name in os.listdir(RAW_FOLDER):          # test: only 3 files first
    with open(f"{RAW_FOLDER}/{name}", "rb") as f:
        w.files.upload(f"{VOLUME}/{name}", f, overwrite=True)
    print("uploaded", name)
