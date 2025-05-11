
"""
clean-postcodes.py

This script processes the Scottish Postcode Directory (SPD) CSV file to extract and filter
postcode data for Glasgow City Council. It outputs a lightweight, application-ready
Parquet file containing postcode, latitude, and longitude fields. In future development
this will be replaced with an address lookup.

Usage:
    - The Scottish Postcode Directory is available on nrsscotland.gov.uk
    - The January 2025 version was here: https://www.nrscotland.gov.uk/publications/scottish-postcode-directory-2025/
    - Under Data Download download the Postcode Index
    - Place the whole folder inside: raw-data/scottish-postcode-directory/spd_2025-01 updating the yyyy-mm as appropriate
    - Update INPUT_FOLDER path below
    - Run the script from the project root: python scripts/clean-postcodes.py
    - Output will be saved to: data/postcodes.parquet

Author: Neil Currie
Project: ReportCard
License: See README.md
"""

# Imports

import pandas as pd
import os

# Paths

INPUT_DIR = "raw-data/scottish-postcode-directory/spd_2025-01"
SPD_FILES = ["SmallUser.csv", "LargeUser.csv"]

OUTPUT_FILE = "data/postcodes.parquet"

# Read data and transform

dfs = []

for file in SPD_FILES:
    path = os.path.join(INPUT_DIR, file)
    if os.path.exists(path):
        df = pd.read_csv(path, usecols=["Postcode", "Latitude", "Longitude", "CouncilArea2019Code"])
        df = df.rename(columns={
            "Postcode": "postcode",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "CouncilArea2019Code": "local_authority"
        })
        dfs.append(df)

postcodes_df = pd.concat(dfs, ignore_index = True)
postcodes_df = postcodes_df.drop_duplicates(subset= ["postcode", "local_authority"])

# Output the parquet file

os.makedirs("data", exist_ok=True)
df.to_parquet(OUTPUT_FILE, index=False)
