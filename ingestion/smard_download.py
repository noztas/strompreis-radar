import json                       # to write Python objects into a .json file
import os                         # to create folders
import time                       # to pause between downloads
import requests


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


# 1. Which series to download
#     4169 = price, 4068 = solar, 4067 = wind onshore, 1225 = wind offshore, 410 = consumption
SERIES_IDS = [4169, 4068, 4067, 1225, 410]

# 2. Choose the mode
#     "backfill" = all weeks (once, or when a new series is added)
#     "daily"    = only the 2 newest weeks (covers the last 7 days)
MODE = "daily"

# 3. For each series: get its own index, then download the chosen weeks
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
