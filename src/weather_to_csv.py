#!/usr/bin/env python3
"""
parse_weather.py — parser for NOAA daily CDD/HDD raw files
----------------------------------------------------------
Reads ClimateDivisions.Cooling.txt and ClimateDivisions.Heating.txt
for all years under data/raw/weather/, converts to tidy long format,
and outputs combined CSVs:
  - data/processed/weather_cdd.csv
  - data/processed/weather_hdd.csv

Usage
-----
$ python src/parse_weather.py
"""
import pandas as pd
from pathlib import Path
import glob

RAW_ROOT = Path('data/raw/weather')
OUT_DIR = Path('data/processed')
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Function to parse one file
def parse_file(path: Path):
    """Parse a NOAA ClimateDivisions file into long-format DataFrame."""
    # Read all lines from the file
    lines = path.read_text().splitlines()
    # Find header line starting with 'Region|'
    header_idx = next(i for i, l in enumerate(lines) if l.startswith('Region|'))
    # Extract column names
    header = lines[header_idx].split('|')
    dates = header[1:]
    # Parse subsequent lines where first char is digit (region code)
    data = []
    for l in lines[header_idx+1:]:
        if not l or not l[0].isdigit():
            continue
        parts = l.split('|')
        region = parts[0]
        values = parts[1:]
        for date_str, val_str in zip(dates, values):
            try:
                val = float(val_str)
            except ValueError:
                continue
            data.append((region, date_str, val))
    # Build DataFrame
    df = pd.DataFrame(data, columns=['region', 'date', 'value'])
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    return df


def main():
    # Collect cooling and heating
    cooling_frames = []
    heating_frames = []
    for year_dir in sorted(RAW_ROOT.iterdir()):
        if not year_dir.is_dir():
            continue
        cool_path = year_dir / 'ClimateDivisions.Cooling.txt'
        heat_path = year_dir / 'ClimateDivisions.Heating.txt'
        if cool_path.exists():
            cooling_frames.append(parse_file(cool_path))
        if heat_path.exists():
            heating_frames.append(parse_file(heat_path))

    # Concatenate all years
    df_cdd = pd.concat(cooling_frames, ignore_index=True)
    df_hdd = pd.concat(heating_frames, ignore_index=True)

    # Save individual
    df_cdd.to_csv(OUT_DIR / 'weather_cdd.csv', index=False)
    df_hdd.to_csv(OUT_DIR / 'weather_hdd.csv', index=False)

    # Merge into wide daily with region dimension
    # e.g., pivot if needed or aggregate
    # Example: national average
    cdd_daily = df_cdd.groupby('date')['value'].mean().reset_index().rename(columns={'value':'CDD'})
    hdd_daily = df_hdd.groupby('date')['value'].mean().reset_index().rename(columns={'value':'HDD'})
    weather = pd.merge(cdd_daily, hdd_daily, on='date')
    weather.to_csv(OUT_DIR / 'weather_agg.csv', index=False)

    print('✅ Parsed and saved:',
          'weather_cdd.csv, weather_hdd.csv, weather_agg.csv')

if __name__ == '__main__':
    main()
