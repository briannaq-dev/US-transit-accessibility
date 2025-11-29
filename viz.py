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
    column="Pct_Jobs_byTr_av",
    cmap="viridis",
    scheme="Quantiles",
    k=4,
    legend=True,
    legend_kwds={
        "title": "Average % of Jobs Reachable (≤45 min Transit)",
        "bbox_to_anchor": (1.15, 1),
        "fmt": "{:.2f}"
    },
    ax=ax
)

plt.title("Average % of Jobs Reachable (≤45 min Transit) in Massachusetts Metro Areas")
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
    column="Pct_Jobs_byTr_av",
    cmap="viridis",
    scheme="Quantiles",
    k=4,
    legend=True,
    legend_kwds={
        "title": "Average % of Jobs Reachable (≤45 min Transit)",
        "bbox_to_anchor": (1.15, 1),
        "fmt": "{:.2f}"
    },
    ax=ax
)

plt.title("Average % of Jobs Reachable (≤45 min Transit) in Oregon Metro Areas")
plt.axis("off")
plt.tight_layout()
plt.savefig("outputs/map_accessibility_or.png", bbox_inches="tight", dpi=300)
plt.show()

# Slider for NatWalkInd vs. Average % of Zero-Car Households
slider = alt.binding_range(min = 10000, max = 21000000, step = 10000, name = "Cutoff (Population Size): ")
selection = alt.param(bind = slider, value = 100000)

slider_nwi_zerocar = alt.Chart(agg_walk).mark_circle().encode(
    x = alt.X('avg_NWI:Q', title = 'Walkability Score'),
    y = alt.Y('calc_avg_pct_zero_car_HH:Q', title = 'Average % Zero-Car Households'),
    color = alt.condition(
        alt.datum.avg_population < selection, 
        alt.value('gray'),
        alt.value('blue') 
    ),
    tooltip=[
            alt.Tooltip('CBSA_Name:N', title='Metro Area'),
            alt.Tooltip('calc_avg_pct_zero_car_HH:Q', title='Average % Zero-Car Households'),
            alt.Tooltip('avg_NWI:Q', title='Average National Walkability Index'),
            alt.Tooltip('avg_population:Q', title='Population')
    ]
).transform_calculate(
    calc_avg_pct_zero_car_HH="datum.avg_pct_zero_car_HH * 100"
).properties(
    title = "Walkability Score vs. Zero-Car Households across several metro areas"
).add_params(selection
)

slider_nwi_zerocar.save("outputs/slider_scatterplot_zero_car.html")

# Filtering data by the state (STATEFP Column)
input_dropdown = alt.binding_select(options = [None, 1, 2, 4
                                               , 5, 6, 8, 9
                                               , 10, 11, 12, 13, 15
                                               , 16, 17, 18, 19, 20
                                               , 21, 22, 23, 24, 25, 26
                                               , 27, 28, 29, 30, 31
                                               , 32, 33, 34, 35, 36
                                               , 37, 38, 39, 40, 41
                                               , 42, 44, 45, 46
                                               , 47, 48, 49, 50, 51
                                               , 53, 54, 55, 56],
                                    labels = ['All', 'Alabama', 'Alaska', 'Arizona', 'Arkansas',
                                              'California', 'Colorado', 'Connecticut', 'Delaware',
                                              'District of Columbia', 'Florida', 'Georgia', 'Hawaii',
                                              'Idaho', 'Illinois', 'Indiana', 'Iowa',
                                              'Kansas', 'Kentucky', 'Louisiana', 'Maine',
                                              'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
                                              'Mississippi', 'Missouri', 'Montana', 'Nebraska',
                                              'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
                                              'New York', 'North Carolina', 'North Dakota', 'Ohio',
                                              'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
                                              'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
                                              'Utah', 'Vermont', 'Virginia', 'Washington',
                                              'West Virginia', 'Wisconsin', 'Wyoming'],
                                     name = "State: " )

selection2 = alt.selection_point(fields = ['state_fp'], bind = input_dropdown)

select_state = alt.Chart(agg_walk).mark_circle().encode(
    x = alt.X('avg_NWI:Q', title="Walkability Score"),
    y = alt.Y('avg_D1B:Q', title="Population Density"),
    color = alt.condition(selection2, alt.value('blue'), alt.value('grey')),
    opacity = alt.condition(selection2, alt.value(1), alt.value(0.1)),
    tooltip=[
            alt.Tooltip('CBSA_Name:N', title='Metro Area'),
            alt.Tooltip('avg_NWI:Q', title='Walkability Score'),
            alt.Tooltip('avg_D1B:Q', title='Population Density'),
            alt.Tooltip('avg_population:Q', title='Population')
    ]
).add_params(
    selection2
).properties(
    title = "Walkability vs. Population Density"
)

select_state.save("outputs/select_state.html")

print("Visualizations saved to outputs:")
print(" - map_accessibility.png")
print(" - map_accessibility_ma.png")
print(" - map_accessibility_or.png")
print(" - top10_metros_jobs.png")
print(" - scatter_access_vs_jobs.png")
print(" - interactive_bar.html")