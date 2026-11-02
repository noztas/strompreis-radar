# Databricks notebook source
# Load all SMARD JSON files from the landing volume into the Bronze table.
# Auto Loader remembers which files it already loaded (checkpoint),
# so every run adds only new files.

LANDING = "/Volumes/energy/bronze/landing"                 # where the JSON files are
CHECKPOINT = "/Volumes/energy/bronze/checkpoints/smard_raw" # Auto Loader's memory
TABLE = "energy.bronze.smard_raw"                          # where the rows go

# COMMAND ----------

df = (
    spark.readStream
    .format("cloudFiles")                            # cloudFiles = Auto Loader
    .option("cloudFiles.format", "json")             # the files are JSON
    .option("cloudFiles.schemaLocation", CHECKPOINT) # where it saves the column list it found
    .load(LANDING)
)

# COMMAND ----------

(
    df.writeStream
    .option("checkpointLocation", CHECKPOINT)  # where it saves the list of loaded files
    .trigger(availableNow=True)                # load all new files, then stop
    .toTable(TABLE)
)
