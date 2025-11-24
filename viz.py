import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from vega_datasets import data

# Load cleaned data
csv_path = "outputs/cleaned_transit_data.csv"
geojson_path = "outputs/cleaned_transit_data.geojson"
agg_path = "outputs/metro_aggregated.csv"

df = pd.read_csv(csv_path)
gdf = gpd.read_file(geojson_path)
agg = pd.read_csv(agg_path)

# Scatterplot -  Average Accessibility Index vs. Average % Job Accessibility by Transit
scatterplotChart = (
    alt.Chart(agg).mark_point().encode(
        x=alt.X('avg_access:Q', title="Average Accessibility Index"),
        y=alt.Y('avg_jobs:Q', title="Average % Job Accessibility by Transit"),
        tooltip=[
            alt.Tooltip('CBSA_Name:N', title='Metro Area'),
            alt.Tooltip('avg_access:Q', title='Accessibility Index'),
            alt.Tooltip('avg_jobs:Q', title='% Jobs Reachable by Transit')
        ]
    ).properties(
    title = "The Average Accessibility Index vs. Average % Job Accessibility by Transit"
))

scatterplotChart.save("outputs/scatter_access_vs_jobs.html")

# Bar Chart - Top 10 Metro Areas
top10 = agg.sort_values("avg_jobs", ascending=False).head(10)
sns.barplot(y="CBSA_Name", x="avg_jobs", data=top10, dodge=False, legend=False)
plt.title("Top 10 Metro Areas: Job Accessibility via Transit")
plt.grid(axis="x", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.xlabel("Average % of Jobs Reachable (≤45 min Transit)")
plt.tight_layout()
plt.savefig("outputs/top10_metros_bar.png")
plt.show()

# Barplot - Top 10 Low Wage Worker Job Accessibility by Transit
sns.barplot(y="CBSA_Name", x="avg_LoWgWrks_byTr", data=top10, dodge=False, legend=False)
plt.title("Top 10 Metro Areas: Low Wage Worker Job Accessibility via Transit (≤45 min Transit)")
plt.grid(axis="x", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.xlabel("Average Amount of Low-Wage Jobs Reachable")
plt.tight_layout()
plt.savefig("outputs/top10_lowgwrks_bar.png")
plt.show()

# Choropleth - Massachusetts Accessibility Index
ma_metros = ['Boston-Cambridge-Quincy, MA-NH',
            'Providence-New Bedford-Fall River, RI-MA',
            'Barnstable Town, MA',
            'Pittsfield, MA',
            'Springfield, MA',
            'Worcester, MA']

ma_gdf = gdf[gdf['CBSA_Name'].isin(ma_metros)]

fig, ax = plt.subplots(figsize=(6, 6))
ma_gdf.plot(
    column="TrAccess_Index",
    cmap="viridis",
    scheme="Quantiles",
    k=4,
    legend=True,
    legend_kwds={
        "title": "Transit Accessibility Index",
        "bbox_to_anchor": (1.15, 1),
        "fmt": "{:.2f}"
    },
    ax=ax
)

plt.title("Transit Accessibility Index - Massachusetts Metro Areas")
plt.axis("off")
plt.tight_layout()
plt.savefig("outputs/map_accessibility_ma.png", bbox_inches="tight", dpi=300)
plt.show()

print("Visualizations saved to outputs:")
print(" - map_accessibility.png")
print(" - map_accessibility_ma.png")
print(" - top10_metros_jobs.png")
print(" - scatter_access_vs_jobs.png")