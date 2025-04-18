import pandas as pd
import requests
from io import BytesIO
import os

URL = "https://www.norskpetroleum.no/generator/csv.php?lang=en&from=query&dataSource=production&title=Annual+production&groupBy=year&orderBy=1&orderByAscending=1"
OUTPUT_PATH = "public/assets/data/annual_historical_production.csv"

print("- Downloading Excel from NorskPetroleum...")
res = requests.get(URL)

if res.status_code != 200:
    raise Exception(f"- Failed to download data: {res.status_code}")

wb = BytesIO(res.content)
df = pd.read_excel(wb, header=2)  # Using 3rd row as header

print("- Columns in Excel file:")
print("-", df.columns.tolist())

print("- Renaming Norwegian columns to English...")
df = df.rename(columns={
    "År": "year",
    "Olje": "oil",
    "Gass": "gas",
    "Kondensat": "condensate",
    "NGL": "ngl"
})

print("- Cleaning data...")
df = df[["year", "oil", "gas", "condensate", "ngl"]].dropna(how="all")
df = df.astype({"year": int, "oil": float, "gas": float, "condensate": float, "ngl": float})
df = df[:-1] # Remove last row (current year)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"- Saved CSV to: {OUTPUT_PATH}")