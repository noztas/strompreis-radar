import requests
from datetime import datetime


def download_week(series_id, ts):
    """Download one week of SMARD data and return it as a Python object."""
    week_url = f"https://www.smard.de/app/chart_data/{series_id}/DE-LU/{series_id}_DE-LU_hour_{ts}.json"
    response = requests.get(week_url)
    return response.json()


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
