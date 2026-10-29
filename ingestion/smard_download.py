import json                       # to write Python objects into a .json file
import os                         # to create folders
import time                       # to pause between downloads
import requests
from datetime import datetime


def download_week(series_id, ts):
    """Download one week of SMARD data and return it as a Python object."""
    week_url = f"https://www.smard.de/app/chart_data/{series_id}/DE-LU/{series_id}_DE-LU_hour_{ts}.json"
    response = requests.get(week_url)
    return response.json()


# Save one week to a file. Same series + same week = same file name,
# so running it again overwrites the file instead of making a copy (idempotent).
def save_week(week_data, series_id, ts):
    """Save one week of data as data/raw/<series_id>_<ts>.json and return the path."""
    folder = "data/raw"
    os.makedirs(folder, exist_ok=True)          # create the folder; no error if it already exists
    path = f"{folder}/{series_id}_{ts}.json"
    with open(path, "w") as f:                  # "w" = write (overwrite if the file exists)
        json.dump(week_data, f)
    return path


# 1. The address of the index file (the "table of contents")
url = "https://www.smard.de/app/chart_data/4169/DE-LU/index_hour.json"

# 2. Ask SMARD for the file
response = requests.get(url)

# 3. Turn the JSON text into a Python object
data = response.json()

# 4. Take the list of timestamps out of it
timestamps = data["timestamps"]

# 5. Count and show the results
print("Number of weeks:", len(timestamps))
print("First week:", datetime.fromtimestamp(timestamps[0] / 1000))
print("Last week:", datetime.fromtimestamp(timestamps[-1] / 1000))

# 6. Download the LAST week using our function
last_ts = timestamps[-1]
week_data = download_week(4169, last_ts)
rows = week_data["series"]      # list of [timestamp, price] pairs

# 7. Count all rows, and count the missing prices (None)
missing = 0
for row in rows:
    if row[1] is None:
        missing = missing + 1

print("Rows in this week:", len(rows))
print("Missing prices:", missing)

# 8. Show the first hour
print("First hour:", datetime.fromtimestamp(rows[0][0] / 1000), "→", rows[0][1], "€/MWh")

# 9. Save the week to a file
saved_path = save_week(week_data, 4169, last_ts)
print("Saved to:", saved_path)

# 10. Choose which weeks to download
#     "backfill" = all weeks (only once at the start)
#     "daily"    = only the 2 newest weeks (covers the last 7 days)
MODE = "daily"

if MODE == "backfill":
    weeks_to_download = timestamps
else:
    weeks_to_download = timestamps[-2:]

print("Mode:", MODE, "→ weeks to download:", len(weeks_to_download))

# 11. Download and save the chosen weeks
for ts in weeks_to_download:
    week_data = download_week(4169, ts)
    path = save_week(week_data, 4169, ts)
    print("Saved:", path)
    time.sleep(0.5)
