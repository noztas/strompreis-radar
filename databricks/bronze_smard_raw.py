# Databricks notebook source
# Load all SMARD JSON files from the landing volume into the Bronze table.
# Auto Loader remembers which files it already loaded (checkpoint),
# so every run adds only new files.

LANDING = "/Volumes/energy/bronze/landing"                 # where the JSON files are
CHECKPOINT = "/Volumes/energy/bronze/checkpoints/smard_raw" # Auto Loader's memory
TABLE = "energy.bronze.smard_raw"                          # where the rows go

# COMMAND ----------

from pyspark.sql.functions import col, current_timestamp

df = (
    spark.readStream
    .format("cloudFiles")                            # cloudFiles = Auto Loader
    .option("cloudFiles.format", "json")             # the files are JSON
    .option("cloudFiles.schemaLocation", CHECKPOINT) # where it saves the column list it found
    .load(LANDING)
    .select(
        "*",                                               # keep all columns from the JSON
        col("_metadata.file_path").alias("_source_file"),  # which file the row came from
        current_timestamp().alias("_load_ts"),             # when the row was loaded
    )
)

# COMMAND ----------

(
    df.writeStream
    .option("checkpointLocation", CHECKPOINT)  # where it saves the list of loaded files
    .trigger(availableNow=True)                # load all new files, then stop
    .toTable(TABLE)
)
