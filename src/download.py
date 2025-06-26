#!/usr/bin/env python3
"""download.py — data‑pull utility for Natural‑Gas forecasting project
--------------------------------------------------------------------
Pulls and saves tidy CSVs into `data/processed/`.

Usage
-----
$ python src/download.py              # Henry Hub & WTI

Dependencies
------------
• pandas
• python-dotenv
• fredapi
• certifi      # SSL certificates on macOS

Environment
-----------
Create an `.env` file at the repo root with:
    FRED_API_KEY=<your FRED API key>

Notes
-----
• Fetches daily Henry Hub & WTI spot prices via FRED.
"""

import os
import ssl
from pathlib import Path
import argparse

import pandas as pd
from dotenv import load_dotenv
from fredapi import Fred
import certifi

# SSL fix for macOS
os.environ['SSL_CERT_FILE'] = certifi.where()
ssl._create_default_https_context = ssl.create_default_context

# Load environment variables
load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
FRED_API_KEY = os.getenv("FRED_API_KEY")
if not FRED_API_KEY:
    raise RuntimeError("FRED_API_KEY not set — add to your .env file")

# FRED Series IDs
HENRY_SERIES = "DHHNGSP"      # Daily Henry Hub spot price
WTI_SERIES = "DCOILWTICO"     # Daily WTI crude oil spot price

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def pull_fred_series(series_id: str, col_name: str) -> pd.DataFrame:
    """Download a FRED series and return tidy DataFrame."""
    fred = Fred(api_key=FRED_API_KEY)
    series = fred.get_series(series_id)
    df = series.to_frame(col_name)
    df.index.name = "date"
    df.reset_index(inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    return df


def save_csv(df: pd.DataFrame, filename: str) -> None:
    """Save DataFrame to data/processed/filename.csv, creating dirs as needed."""
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / filename, index=False)

# ---------------------------------------------------------------------------
# Main fetch logic
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Download Henry Hub & WTI spot prices from FRED.")
    args = parser.parse_args()

    # Henry Hub
    hh = pull_fred_series(HENRY_SERIES, "HH_spot")
    save_csv(hh, "henry_hub_spot.csv")
    print(f"✔ Henry Hub rows: {len(hh):,}")

    # WTI
    wti = pull_fred_series(WTI_SERIES, "WTI_spot")
    save_csv(wti, "wti_spot.csv")
    print(f"✔ WTI rows: {len(wti):,}")


if __name__ == "__main__":
    main()
