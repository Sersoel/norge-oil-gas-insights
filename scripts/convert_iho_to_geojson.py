import geopandas as gpd
import pandas as pd
import os

IHO_SHP = "data/raw/iho/Intersect_EEZ_IHO_v5_20241010/Intersect_EEZ_IHO_v5_20241010.shp"
PRODUCTION_CSV = "data/processed/production_per_sea.csv"
OUTPUT_GEOJSON = "data/processed/area_production.geojson"

print("- Loading shapefile...")
gdf = gpd.read_file(IHO_SHP)

print("- Filtering for relevant sea areas...")
target_names = ["North Sea", "Norwegian Sea", "Barentsz Sea"]
subset = gdf[gdf["IHO_Sea"].isin(target_names)].copy()

print("- Loading area production values from cleaned CSV...")
prod_df = pd.read_csv(PRODUCTION_CSV)
prod_df["area"] = prod_df["area"].str.strip()

print("- Merging totals into GeoJSON features...")
subset_unique = subset.drop_duplicates(subset=["IHO_Sea"]).copy()
merged = subset.merge(
    prod_df[["area", "total_oil_equivalents"]],
    left_on="IHO_Sea", right_on="area", how="left"
)
merged = merged.drop(columns=["area"])
merged = merged.rename(columns={"total_oil_equivalents": "total_production"})

if merged["total_production"].isna().any():
    print("Warning: Some areas have missing production values.")
    print(merged[merged["total_production"].isna()][["IHO_Sea"]])

print("- Writing to GeoJSON...")
os.makedirs(os.path.dirname(OUTPUT_GEOJSON), exist_ok=True)
merged.to_file(OUTPUT_GEOJSON, driver="GeoJSON")

print(f"- GeoJSON saved: {OUTPUT_GEOJSON}")