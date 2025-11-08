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

# Top 3 States Choropleth Maps
# top3_metros = top10["CBSA_Name"].head(3).tolist()

# for metro in top3_metros:
#     subset = gdf[gdf["CBSA_Name"] == metro]
#     if subset.empty:
#         continue

#     fig, ax = plt.subplots(figsize=(8, 6))
#     subset.plot(
#         column="TrAccess_Index",
#         cmap="YlGnBu",
#         scheme="Quantiles",
#         k=4,
#         legend=True,
#         legend_kwds={
#             "title": f"Transit Accessibility Index – {metro}",
#             "fmt": "{:.2f}",
#             "bbox_to_anchor": (1.05, 1)
#         },
#         ax=ax
#     )
#     plt.title(f"Transit Accessibility – {metro}", fontsize=12)
#     plt.axis("off")
#     plt.tight_layout()
#     filename = f"outputs/map_accessibility_{metro.replace(',', '').replace(' ', '_')}.png"
#     plt.savefig(filename, bbox_inches="tight", dpi=300)
#     plt.close()
#     print(f"✅ Saved {filename}")

'''
# Transit Accessibility Index Choropleth Map
fig, ax = plt.subplots(figsize=(14,6))
gdf.plot(
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
plt.title("Transit Accessibility Index by CBG")
plt.axis("off")
plt.tight_layout()
plt.savefig("outputs/map_accessibility.png", bbox_inches="tight")
plt.show()
'''

# Accessibility vs. Job Reachability Scatterplot
# sns.scatterplot(x="avg_access", y="avg_jobs", data=agg, color="seagreen", alpha=0.7)
# plt.title("Transit Accessibility vs. Job Reachability by Metro Area")
# plt.xlabel("Average Accessibility Index")
# plt.ylabel("Average % of Jobs Reachable")
# plt.tight_layout()
# plt.savefig("outputs/scatter_access_vs_jobs.png")
# plt.show()

print("Visualizations saved to outputs:")
print(" - map_accessibility.png")
print(" - top10_metros_jobs.png")
print(" - scatter_access_vs_jobs.png")