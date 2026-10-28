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
