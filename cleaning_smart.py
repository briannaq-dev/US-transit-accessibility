import pandas as pd
import numpy as np
from scipy.stats import zscore
import re
import os

# --- Step 1: Load CSV data ---
csv_path = "outputs/smartlocation.csv"  # your CSV file
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found: {csv_path}")

df = pd.read_csv(csv_path)
print(f"✅ Loaded CSV with {len(df)} rows")

# --- Step 2: Clean and prepare the data ---
numeric_cols = [c for c in df.columns if c not in ['CBSA_Name', 'CBSA', 'GEOID10', 'CBG_ID']]
for c in numeric_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

if 'NatWalkInd' in df.columns:
    df.loc[df['NatWalkInd'] < 0, 'NatWalkInd'] = np.nan
    df['NatWalkInd_z'] = zscore(df['NatWalkInd'].fillna(df['NatWalkInd'].mean()))

pct_cols = [c for c in df.columns if re.search(r'pct|percent|Pct', c, re.IGNORECASE)]
for c in pct_cols:
    df[c + "_z"] = zscore(df[c].fillna(df[c].mean()))

# --- Step 3: Aggregate by metro area ---
group = df.groupby('CBSA_Name', dropna=True)
agg = group.agg(
    metro_count=('GEOID10', 'count'),
    # Population Density
    avg_D1B=('D1B', 'mean') if 'D1B' in df.columns else ('D1B', 'mean'),
    # National Walkability Index
    avg_NWI=('NatWalkInd', 'mean') if 'NatWalkInd' in df.columns else ('NatWalkInd', 'mean'),
    # Percent of Zero-Car Households
    avg_pct_zero_car_HH=('Pct_AO0', 'mean') if 'Pct_AO0' in df.columns else ('Pct_AO0', 'mean')
    
).reset_index()

# --- Step 4: Export results ---
os.makedirs("outputs", exist_ok=True)
df.to_csv("outputs/cleaned_smart_data.csv", index=False)
agg.to_csv("outputs/smart_aggregated.csv", index=False)

print("\nSaved files:")
print(" - outputs/cleaned_smart_data.csv")
print(" - outputs/smart_aggregated.csv")