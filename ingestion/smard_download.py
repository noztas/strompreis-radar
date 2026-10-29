import json                       # to write Python objects into a .json file
import os                         # to create folders
import time                       # to pause between downloads
import requests
from datetime import datetime


def get_json(url, retries=3):
    """Download a URL and return its JSON. Try up to 3 times if it fails."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=30)   # wait at most 30 seconds
            response.raise_for_status()                # treat errors like 404/500 as failures too
            return response.json()                     # success → leave the function
        except requests.exceptions.RequestException as error:
            print(f"  Attempt {attempt} of {retries} failed: {error}")
            if attempt == retries:
                raise                                  # 3rd failure → really stop
            time.sleep(5)                              # wait a bit, then try again


def download_week(series_id, ts):
    """Download one week of SMARD data and return it as a Python object."""
    week_url = f"https://www.smard.de/app/chart_data/{series_id}/DE-LU/{series_id}_DE-LU_hour_{ts}.json"
    return get_json(week_url)


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


def get_timestamps(series_id):
    """Download the index of one series and return its list of week timestamps."""
    index_url = f"https://www.smard.de/app/chart_data/{series_id}/DE-LU/index_hour.json"
    return get_json(index_url)["timestamps"]


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

# 10. Which series to download
#     4169 = price, 4068 = solar, 4067 = wind onshore, 1225 = wind offshore, 410 = consumption
SERIES_IDS = [4169, 4068, 4067, 1225, 410]

# 11. Choose the mode
#     "backfill" = all weeks (once, or when a new series is added)
#     "daily"    = only the 2 newest weeks (covers the last 7 days)
MODE = "daily"

# 12. For each series: get its own index, then download the chosen weeks
for series_id in SERIES_IDS:
    series_timestamps = get_timestamps(series_id)

    if MODE == "backfill":
        weeks_to_download = series_timestamps
    else:
        weeks_to_download = series_timestamps[-2:]

    print("Series", series_id, "| mode:", MODE, "→ weeks to download:", len(weeks_to_download))

    for ts in weeks_to_download:
        week_data = download_week(series_id, ts)
        path = save_week(week_data, series_id, ts)
        print("  Saved:", path)
        time.sleep(0.5)
