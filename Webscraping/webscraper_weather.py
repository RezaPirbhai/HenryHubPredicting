#!/usr/bin/env python3
"""
download_weather.py — HTTP scraper for NOAA daily CDD/HDD data
----------------------------------------------------------------
Automatically downloads ClimateDivisions.Cooling.txt and
ClimateDivisions.Heating.txt for each year directory available
on NOAA CPC under daily_data (1997–present) using HTTP.

Usage
-----
$ python Webscraping/webscraper_weather.py

Outputs raw text files to data/raw/weather/<year>/
"""
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup

# Base URL for NOAA CPC daily degree days
BASE_URL = 'https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_data/'
OUTPUT_ROOT = Path('data/raw/weather')
FILES = ['ClimateDivisions.Cooling.txt', 'ClimateDivisions.Heating.txt']

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def list_year_dirs():
    """Fetch index page and parse available year directories."""
    resp = requests.get(BASE_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    years = [a['href'].strip('/') for a in soup.find_all('a', href=True)
             if re.fullmatch(r'\d{4}/', a['href'])]
    return sorted(years)


def download_file(year: str, fname: str):
    """Download a single file for a given year via HTTP."""
    url = f'{BASE_URL}{year}/{fname}'
    local_dir = OUTPUT_ROOT / year
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / fname
    if local_path.exists():
        print(f'✔ Already have {year}/{fname}')
        return
    print(f'⬇ Downloading {year}/{fname}...')
    r = requests.get(url)
    if r.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(r.content)
        print(f'  → Saved to {local_path}')
    else:
        print(f'⚠️ Skipping {year}/{fname}: HTTP {r.status_code}')


def main():
    years = list_year_dirs()
    if not years:
        print('‼ No year directories found at', BASE_URL)
        return
    for year in years:
        print(f'Processing {year}...')
        for fname in FILES:
            download_file(year, fname)
    print('✅ Finished downloading weather files.')


if __name__ == '__main__':
    main()
