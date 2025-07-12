import pandas as pd
import requests
from io import BytesIO
import os
import json
from datetime import datetime

HISTORICAL_PRODUCTION_URL = "https://www.norskpetroleum.no/generator/csv.php?lang=en&from=query&dataSource=production&title=Annual+production&groupBy=year&orderBy=1&orderByAscending=1"
PRODUCTION_PER_SEA_URL = "https://www.norskpetroleum.no/generator/csv.php?lang=en&from=query&dataSource=production&title=Total+production+per+sea+area+at+year-end+2024&groupBy=area&orderBy=6&filterProductionYearTo=2024"
HISTORICAL_PRODUCTION_OUTPUT_PATH = "data/processed/annual_historical_production.csv"
PRODUCTION_PER_SEA_OUTPUT_PATH = "data/processed/production_per_sea.csv"
HISTORICAL_PRODUCTION_OUTPUT_META = "data/processed/metadata.json"

import os
import pandas as pd
import requests
from io import BytesIO


NORWEGIAN_TO_ENGLISH = {
    "År": "year",
    "Olje": "oil",
    "Gass": "gas",
    "Kondensat": "condensate",
    "NGL": "ngl",
    "Sum oljeekvivalenter": "total_oil_equivalents",
    "Område": "area"
}

def fetch_production_from_excel(
    url: str,
    output_path: str,
    column_mapping: dict = None,
    start_row: int = 0,
    exclude_last_row: bool = False # Remove last row (current year)
):
    print(f"- Downloading production data from: {url}")
    res = requests.get(url)

    if res.status_code != 200:
        raise Exception(f"- Failed to download data: {res.status_code}")

    print("- Reading Excel content...")
    df = pd.read_excel(BytesIO(res.content), skiprows=start_row)

    print("- Columns in Excel file:")
    print("-", df.columns.tolist())

    print("- Renaming Norwegian columns to English...")
    # print("-", df.columns.tolist())

    # Use default mapping if none provided
    column_mapping = column_mapping or NORWEGIAN_TO_ENGLISH

    # Translate columns
    renamed_cols = {col: column_mapping[col] for col in df.columns if col in column_mapping}
    df = df.rename(columns=renamed_cols)

    if exclude_last_row:
        print("- Excluding last row...")
        df = df[:-1]
        # df = df.iloc[:-1]

    # Drop rows with all NaNs in relevant columns
    kept_columns = list(renamed_cols.values())
    df = df[kept_columns].dropna(how="all")

    # Attempt type casting
    for col in kept_columns:
        if col != "area":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "area" in df.columns:
        df["area"] = df["area"].astype(str)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"- Saved cleaned CSV to: {output_path}")
    print("- Done.")

if __name__ == "__main__":

    fetch_production_from_excel(
        url=HISTORICAL_PRODUCTION_URL, 
        output_path=HISTORICAL_PRODUCTION_OUTPUT_PATH,
        column_mapping=None,
        start_row=2,  # Using 3rd row as header
        exclude_last_row=True # Remove last row (current year)
        )
    
    metadata = {
        "source": HISTORICAL_PRODUCTION_URL,
        "fetched_at": datetime.utcnow().isoformat(timespec='seconds') + "Z"
    }
    with open(HISTORICAL_PRODUCTION_OUTPUT_META, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"+ Saved metadata to: {HISTORICAL_PRODUCTION_OUTPUT_META}")

    fetch_production_from_excel(
        url=PRODUCTION_PER_SEA_URL, 
        output_path=PRODUCTION_PER_SEA_OUTPUT_PATH,
        column_mapping=None,
        start_row=4,  # Using 5th row as header
        exclude_last_row=False
        )