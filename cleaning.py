import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.stats import zscore
import re
import os
import zipfile
import tempfile
import shutil

# --- Step 1: Unzip the .gdb.zip file ---
zip_path = "SLD_Trans45.gdb.zip"  # your zipped geodatabase
if not os.path.exists(zip_path):
    raise FileNotFoundError(f"Zip file not found: {zip_path}")

temp_dir = tempfile.mkdtemp()
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(temp_dir)

# Find the .gdb directory inside the extracted files
gdb_candidates = [
    os.path.join(temp_dir, f)
    for f in os.listdir(temp_dir)
    if f.endswith(".gdb") and os.path.isdir(os.path.join(temp_dir, f))
]

if not gdb_candidates:
    raise FileNotFoundError("No .gdb directory found inside the .zip file.")
gdb_path = gdb_candidates[0]

print(f"✅ Extracted GDB found at: {gdb_path}")

# --- Step 2: Load data ---
layer_name = "CBG_Trans45"
gdf = gpd.read_file(gdb_path, layer=layer_name)

# --- Step 3: Clean and prepare the data ---
drop_cols = [c for c in gdf.columns if re.search(r'Shape|geometry|Area|Length', c, re.IGNORECASE)]
df = gdf.drop(columns=drop_cols, errors="ignore")

numeric_cols = [c for c in df.columns if c not in ['CBSA_Name', 'CBSA', 'GEOID10', 'CBG_ID']]
for c in numeric_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

if 'TrAccess_Index' in df.columns:
    df.loc[df['TrAccess_Index'] < 0, 'TrAccess_Index'] = np.nan
    gdf['TrAccess_Index'] = df['TrAccess_Index']
    df['TrAccess_Index_z'] = zscore(df['TrAccess_Index'].fillna(df['TrAccess_Index'].mean()))

pct_cols = [c for c in df.columns if re.search(r'pct|percent|Pct', c, re.IGNORECASE)]
for c in pct_cols:
    df[c + "_z"] = zscore(df[c].fillna(df[c].mean()))

group = df.groupby('CBSA_Name', dropna=True)
agg = group.agg(
    metro_count=('GEOID10', 'count'),
    avg_access=('TrAccess_Index', 'mean'),
    avg_pop=('Pct_Pop_byTr_av', 'mean') if 'Pct_Pop_byTr_av' in df.columns else ('Pct_Pop_byTr', 'mean'),
    avg_jobs=('Pct_Jobs_byTr_av', 'mean') if 'Pct_Jobs_byTr_av' in df.columns else ('Pct_Jobs_byTr', 'mean'),
).reset_index()

# --- Step 4: Export cleaned data ---
os.makedirs("outputs", exist_ok=True)
df.drop(columns=['geometry'], errors='ignore').to_csv("outputs/cleaned_transit_data.csv", index=False)
gdf.to_file("outputs/cleaned_transit_data.geojson", driver="GeoJSON")
agg.to_csv("outputs/metro_aggregated.csv", index=False)

print("\nSaved files:")
print(" - outputs/cleaned_transit_data.csv")
print(" - outputs/cleaned_transit_data.geojson")
print(" - outputs/metro_aggregated.csv")

# --- Step 5: Clean up temporary directory ---
shutil.rmtree(temp_dir)
print(f"\n🧹 Cleaned up temporary folder: {temp_dir}")
