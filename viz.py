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
csv_walk_path = "outputs/smartlocation.csv"
agg_walk_path = "outputs/smart_aggregated.csv"

df = pd.read_csv(csv_path)
df_walk = pd.read_csv(csv_walk_path)
gdf = gpd.read_file(geojson_path)
agg = pd.read_csv(agg_path)
agg_walk = pd.read_csv(agg_walk_path)

# Scatterplot -  Accessibility Score vs. Average % Job Reachable by Transit
scatterplotChart = (
    alt.Chart(agg).mark_point().encode(
        x=alt.X('avg_access:Q', title="Accessibility Score in Metro Area"),
        y=alt.Y(
            'calc_avg_jobs:Q',
            title="Average % Jobs Reachable by Transit"
        ),
        tooltip=[
            alt.Tooltip('CBSA_Name:N', title='Metro Area'),
            alt.Tooltip('avg_access:Q', title='Accessibility Score'),
            alt.Tooltip('calc_avg_jobs:Q', title='% Jobs Reachable by Transit')
        ]
    ).transform_calculate(
        calc_avg_jobs="datum.avg_jobs * 100"
    ).properties(
        title="Accessibility Score vs. Average % Jobs Reachable by Transit"
    )
)

scatterplotChart.save("outputs/scatter_access_vs_jobs.html")

# Scatterplot -  Walkability vs. Population Density
scatterplot_walk_popdensity = (
    alt.Chart(agg_walk).mark_point().encode(
        x=alt.X('avg_D1B:Q', title="Average Population Density"),
        y=alt.Y(
            'avg_NWI:Q',
            title="Average National Walkability Index"
        ),
        tooltip=[
            alt.Tooltip('CBSA_Name:N', title='Metro Area'),
            alt.Tooltip('avg_D1B:Q', title='Average Population Density'),
            alt.Tooltip('avg_NWI:Q', title='Average National Walkability Index')
        ]
    ).properties(
        title="Walkability vs. Population Density"
    )
)

scatterplot_walk_popdensity.save("outputs/scatterplot_walk_popdensity.html")

# Interactive Bar Chart - Comparing Boston to the Top 10 Metro Areas


# Scatterplot -  Zero Car Households
scatterplot_zero_car = (
    alt.Chart(agg_walk).mark_point().encode(
        x=alt.X('avg_pct_zero_car_HH:Q', title="Average % Zero-Car Households"),
        y=alt.Y(
            'avg_NWI:Q',
            title="Average National Walkability Index"
        ),
        tooltip=[
            alt.Tooltip('CBSA_Name:N', title='Metro Area'),
            alt.Tooltip('avg_pct_zero_car_HH:Q', title='Average % Zero-Car Households'),
            alt.Tooltip('avg_NWI:Q', title='Average National Walkability Index')
        ]
    ).transform_calculate(
        calc_avg_pct_zero_car_HH="datum.avg_pct_zero_car_HH * 100"
    ).properties(
        title="Walkability vs. Average % Zero-Car Households"
    )
)

scatterplot_zero_car.save("outputs/scatterplot_zero_car.html")


# Bar Chart - Top 10 Metro Areas
top10 = agg.sort_values("avg_jobs", ascending=False).head(10)
top10["avg_jobs_pct"] = top10["avg_jobs"] * 100
sns.barplot(y="CBSA_Name", x="avg_jobs_pct", data=top10, dodge=False, legend=False)
plt.title("Top 10 Metro Areas: Job Accessibility via Transit")
plt.grid(axis="x", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.ylabel("Metro Area")
plt.xlabel("Average % of Jobs Reachable (≤45 min Transit)")
plt.tight_layout()
plt.savefig("outputs/top10_metros_bar.png")
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

# Oregon Choropleth

or_metros = ['Corvallis, OR',
            'Pendleton-Hermiston, OR',
            'Astoria, OR',
            'Hood River, OR',
            'Eugene-Springfield, OR',
            'Brookings, OR',
            'Medford, OR',
            'Portland-Vancouver-Hillsboro, OR-WA',
            'Pendleton-Hermiston, OR',
            'Salem, OR',
            'Prineville, OR',
            'Coos Bay, OR',
            'La Grande, OR',
            'Roseburg, OR',
            'Albany-Lebanon, OR',
            'The Dalles, OR',
            'Bend, OR',
            'Klamath Falls, OR']

or_gdf = gdf[gdf['CBSA_Name'].isin(or_metros)]

fig, ax = plt.subplots(figsize=(6, 6))
or_gdf.plot(
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

plt.title("Transit Accessibility Index - Oregon Metro Areas")
plt.axis("off")
plt.tight_layout()
plt.savefig("outputs/map_accessibility_or.png", bbox_inches="tight", dpi=300)
plt.show()

print("Visualizations saved to outputs:")
print(" - map_accessibility.png")
print(" - map_accessibility_ma.png")
print(" - map_accessibility_or.png")
print(" - top10_metros_jobs.png")
print(" - scatter_access_vs_jobs.png")
print(" - interactive_bar.html")