-- ============================================================
-- Strompreis-Radar: Databricks setup (Step 1)
-- Creates the catalog, the 3 Medallion schemas and the landing volume.
-- Safe to run again: IF NOT EXISTS skips anything that already exists.
-- Run in: Databricks -> SQL Editor -> Ctrl+A -> Run all
-- ============================================================

-- Catalog = the cabinet for the whole project
CREATE CATALOG IF NOT EXISTS energy;

-- Bronze = raw data, exactly as it came from the SMARD API
CREATE SCHEMA IF NOT EXISTS energy.bronze;

-- Silver = cleaned data: German time, no duplicates, clear column names
CREATE SCHEMA IF NOT EXISTS energy.silver;

-- Gold = report-ready tables (star schema) for Power BI
CREATE SCHEMA IF NOT EXISTS energy.gold;

-- Volume = a folder for files inside bronze; the raw JSON files land here first
CREATE VOLUME IF NOT EXISTS energy.bronze.landing;
