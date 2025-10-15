import pandas as pd
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt

import re

# Read in data
df = pd.read_csv("transit_data.csv")

print(df.head())

#Clean the data
drop_cols = [c for c in df.columns if "Shape" in c or "geometry" in c or "Area" in c or "Length" in c]
df = df.drop(columns=drop_cols, errors="ignore")

for c in df.columns:
    if c not in ['CBSA_Name','CBSA','GEOID10','CBG_ID']:
        df[c] = pd.to_numeric(df[c], errors='coerce')

if 'Access_Index' in df.columns:
    df['Access_Index_z'] = zscore(df['Access_Index'].fillna(df['Access_Index'].mean()))

pct_cols = [c for c in df.columns if re.search(r'pct|percent|Pct', c, re.IGNORECASE)]
for c in pct_cols:
    df[c + "_z"] = zscore(df[c].fillna(df[c].mean()))

group = df.groupby('CBSA_Name', dropna=True)
agg = group.agg(
    metro_count = ('GEOID10','count'),
    avg_access = ('TrAccess_Index','mean'),
    avg_pop = ('Pct_Pop_byTr_av','mean') if 'Pct_Pop_byTr_av' in df.columns else ('Pct_Pop_byTr','mean'),
    avg_jobs = ('Pct_Jobs_byTr_av','mean') if 'Pct_Jobs_byTr_av' in df.columns else ('Pct_Jobs_byTr','mean'),
).reset_index()

#Sort top 5 metro areas
top5 = agg.sort_values('avg_jobs', ascending=False).head(5)

# Plot horizontal bar chart of top 5 Metro Areas
plt.barh(top5['CBSA_Name'], top5['avg_jobs'], color='green')
plt.xlabel("Average proportion")
plt.title("Top 5 Metro Areas: Reachable Within 45 Minutes by Transit")
plt.tight_layout()
plt.savefig("top5_bar.png")
plt.show()

