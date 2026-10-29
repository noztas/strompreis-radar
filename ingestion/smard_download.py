import requests
from datetime import datetime

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

# 6. Build the address of the LAST week's file
last_ts = timestamps[-1]
week_url = f"https://www.smard.de/app/chart_data/4169/DE-LU/4169_DE-LU_hour_{last_ts}.json"

# 7. Download that week
week_response = requests.get(week_url)
week_data = week_response.json()
rows = week_data["series"]      # list of [timestamp, price] pairs
rows
# 8. Count all rows, and count the missing prices (None)
missing = 0
for row in rows:
    if row[1] is None:
        missing = missing + 1

print("Rows in this week:", len(rows))
print("Missing prices:", missing)

# 9. Show the first hour
print("First hour:", datetime.fromtimestamp(rows[0][0] / 1000), "→", rows[0][1], "€/MWh")
