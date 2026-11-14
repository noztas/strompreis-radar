# Writes all German public holidays (national ones) into a dbt seed CSV.
# Run once; run again only if I need more years.
import csv

import holidays

YEARS = range(2016, 2028)    # my data starts Dec 2016; +1 year ahead for the forecast
OUT = "dbt/strompreis_radar/seeds/german_holidays.csv"

de = holidays.Germany(years=YEARS)   # no state given → only holidays for all of Germany

with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["holiday_date", "holiday_name"])    # header row
    for day, name in sorted(de.items()):                 # sorted by date
        writer.writerow([day.isoformat(), name])          # 2026-12-25 → "2026-12-25"

print(f"saved {len(de)} holidays to {OUT}")
