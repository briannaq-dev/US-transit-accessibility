import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.stats import zscore
import re
import os
import zipfile
import tempfile
import shutil

def unzip_gdb(zip_path):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # Find .gdb folder
    gdb_candidates = [
        os.path.join(temp_dir, f)
        for f in os.listdir(temp_dir)
        if f.endswith(".gdb") and os.path.isdir(os.path.join(temp_dir, f))
    ]

    if not gdb_candidates:
        raise FileNotFoundError(f"No .gdb directory found inside {zip_path}")

    gdb_path = gdb_candidates[0]
    print(f"Extracted GDB found at: {gdb_path}")

    return gdb_path, temp_dir

gdb1_path, temp1 = unzip_gdb("SLD_Trans45.gdb.zip")
gdb2_path, temp2 = unzip_gdb("SmartLocationDatabaseV3.zip")

layer_name = "CBG_Trans45"
gdf = gpd.read_file(gdb1_path, layer=layer_name)

smart_layer = "EPA_SLD_Database_V3"
gdf_smart = gpd.read_file(gdb2_path, layer=smart_layer)

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
    avg_pop=('Pct_Pop_byTr', 'mean'),
    avg_jobs=('Pct_Jobs_byTr', 'mean'),
    avg_LoWgWrks_byTr=('LoWgWrks_byTr', 'mean'),
    avg_HiWgWrks_byTr=('HiWgWrks_byTr', 'mean')
).reset_index()

os.makedirs("outputs", exist_ok=True)
df.to_csv("outputs/cleaned_transit_data.csv", index=False)
gdf.to_file("outputs/cleaned_transit_data.geojson", driver="GeoJSON")
agg.to_csv("outputs/metro_aggregated.csv", index=False)
gdf_smart.to_file("outputs/smartlocation.geojson", driver="GeoJSON")
gdf_smart.to_csv("outputs/smartlocation.csv", index=False)
print("Saved SmartLocation dataset.")

shutil.rmtree(temp1)
shutil.rmtree(temp2)