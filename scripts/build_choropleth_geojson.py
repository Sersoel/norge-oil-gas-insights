import geopandas as gpd
import pandas as pd
import os
import sys

# File paths
INPUT_GEOJSON = "data/processed/sea_areas.geojson"
PRODUCTION_CSV = "data/processed/production_per_sea.csv"
OUTPUT_GEOJSON = "data/processed/sea_production.geojson"


def load_sea_areas(filepath):
    print("- Loading sea areas from GeoJSON...")
    gdf = gpd.read_file(filepath)
    gdf["IHO_Sea"] = gdf["IHO_Sea"].str.strip()

    print("- Validating and repairing geometries...")
    gdf["geometry"] = gdf["geometry"].buffer(0)  # Fix potential geometry issues
    return gdf


def load_production_data(filepath):
    print("- Loading production data from CSV...")
    df = pd.read_csv(filepath)
    df["area"] = df["area"].str.strip()
    return df


def merge_datasets(geo_df, prod_df):
    print("- Merging production data with sea areas...")
    merged = geo_df.merge(
        prod_df[["area", "total_oil_equivalents"]],
        left_on="IHO_Sea",
        right_on="area",
        how="left"
    ).drop(columns=["area"]).rename(columns={
        "total_oil_equivalents": "total_production"
    })

    merged["total_production"] = pd.to_numeric(
        merged["total_production"], errors="coerce"
    )

    missing = merged["total_production"].isna()
    if missing.any():
        print("- Warning: Missing production values for the following areas:")
        print(merged.loc[missing, ["IHO_Sea"]])

    return merged


def save_geojson(gdf, output_path):
    print("- Saving merged GeoJSON output...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    gdf.to_file(output_path, driver="GeoJSON")
    print(f"- Output saved to: {output_path}")


def main():
    try:
        sea_gdf = load_sea_areas(INPUT_GEOJSON)
        production_df = load_production_data(PRODUCTION_CSV)
        merged_gdf = merge_datasets(sea_gdf, production_df)
        save_geojson(merged_gdf, OUTPUT_GEOJSON)
    except Exception as e:
        print(f"- Error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()