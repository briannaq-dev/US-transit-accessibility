import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.stats import zscore
import re
import os

# Load data
gdb_path = "SLD_Trans45.gdb"
layer_name = "CBG_Trans45"
gdf = gpd.read_file(gdb_path, layer=layer_name)

# Clean and prepare the data
drop_cols = [c for c in gdf.columns if re.search(r'Shape|geometry|Area|Length', c, re.IGNORECASE)]
df = gdf.drop(columns=drop_cols, errors="ignore")

#Convert numeric columns
numeric_cols = [c for c in df.columns if c not in ['CBSA_Name','CBSA','GEOID10','CBG_ID']]
for c in numeric_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

if 'TrAccess_Index' in df.columns:
    # Replace impossible negative values with NaN
    df.loc[df['TrAccess_Index'] < 0, 'TrAccess_Index'] = np.nan

    # Update GeoDataFrame
    gdf['TrAccess_Index'] = df['TrAccess_Index']

    # Z-score normalization
    df['TrAccess_Index_z'] = zscore(df['TrAccess_Index'].fillna(df['TrAccess_Index'].mean()))

# Z-score normalization for percentage columns
pct_cols = [c for c in df.columns if re.search(r'pct|percent|Pct', c, re.IGNORECASE)]
for c in pct_cols:
    df[c + "_z"] = zscore(df[c].fillna(df[c].mean()))

# Aggregate by metro area
group = df.groupby('CBSA_Name', dropna=True)
agg = group.agg(
    metro_count = ('GEOID10','count'),
    avg_access = ('TrAccess_Index','mean'),
    avg_pop = ('Pct_Pop_byTr_av','mean') if 'Pct_Pop_byTr_av' in df.columns else ('Pct_Pop_byTr','mean'),
    avg_jobs = ('Pct_Jobs_byTr_av','mean') if 'Pct_Jobs_byTr_av' in df.columns else ('Pct_Jobs_byTr','mean'),
).reset_index()

# Create output directory
os.makedirs("outputs", exist_ok=True)

# Export cleaned data
df.drop(columns=['geometry'], errors='ignore').to_csv("outputs/cleaned_transit_data.csv", index=False)
gdf.to_file("outputs/cleaned_transit_data.geojson", driver="GeoJSON")
agg.to_csv("outputs/metro_aggregated.csv", index=False)

print("Saved files:")
print(" - outputs/cleaned_transit_data.csv")
print(" - outputs/cleaned_transit_data.geojson")
print(" - outputs/metro_aggregated.csv")