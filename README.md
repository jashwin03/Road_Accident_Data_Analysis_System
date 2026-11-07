# Project 13 — Road Accident Data Analysis System

Analyse accident records to identify patterns by time, location, vehicle
type, and recorded severity.

> Synthetic / anonymised data only. Findings describe **associations**, not causation.
> No personally identifying data is stored.

## Features
- Import & validate accident records (CSV → SQL)
- Validate date/time, region, vehicle type, severity
- Compare accidents by time period and location
- Summarise severity categories
- Identify periods/locations with higher recorded counts
- Export CSVs, Markdown report, and Matplotlib charts

## Stack
Python · SQLAlchemy · MySQL (or SQLite) · Pandas · NumPy · Matplotlib

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # default: SQLite; edit for MySQL
python main.py all --rows 800
pytest -q