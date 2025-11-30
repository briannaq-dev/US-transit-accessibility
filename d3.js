// This script is used to create the side-by-side bar chart
// that compares the average % of job accessibility among
// low and medium waged workers for each CBSA. To filter,
// we sorted by largest differences between low and medium
// waged workers and selected the top 10.

const transitData = d3.csv("data/metro_aggregated.csv");

transitData.then(function(data) {
  // Convert string values to numbers and calculate difference
  data.forEach(d => {
    d.pct_LoWgWrks_byTr = +d.pct_LoWgWrks_byTr;
    d.pct_MeWgWrks_byTr = +d.pct_MeWgWrks_byTr;
    d.Diff = Math.abs(d.pct_LoWgWrks_byTr - d.pct_MeWgWrks_byTr);
  });

  // Filter out rows with missing data
  const validData = data.filter(d => 
    !isNaN(d.pct_LoWgWrks_byTr) && 
    !isNaN(d.pct_MeWgWrks_byTr) &&
    d.pct_LoWgWrks_byTr > 0 &&
    d.pct_MeWgWrks_byTr > 0
  );

  // Sort by difference and get top 10
  validData.sort((a, b) => b.Diff - a.Diff);
  const top10 = validData.slice(0, 10);

  console.log("Top 10 CBSAs:", top10.map(d => ({ name: d.CBSA_Name, diff: d.Diff })));

  // --- SVG setup ---
  const width = 600, height = 700;
  const margin = { top: 60, bottom: 150, left: 80, right: 40 };

  const svg = d3.select("#barplot")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .style("background", "transparent");

  // --- SCALES ---
  const x0 = d3.scaleBand()
    .domain(top10.map(d => d.CBSA_Name)) 
    .range([margin.left, width - margin.right])
    .padding(0.3);

  const x1 = d3.scaleBand()
    .domain(["LoWgWrks", "MeWgWrks"])
    .range([0, x0.bandwidth()])
    .padding(0.1);

  const y = d3.scaleLinear()
    .domain([0, d3.max(top10, d => Math.max(d.pct_LoWgWrks_byTr, d.pct_MeWgWrks_byTr))])
    .nice()
    .range([height - margin.bottom, margin.top]);

  const color = d3.scaleOrdinal()
    .domain(["LoWgWrks", "MeWgWrks"])
    .range(["#7E3A3A", "#96752C"]);

  // --- AXES ---
  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x0))
    .selectAll("text")
    .attr("transform", "rotate(-45)")
    .attr("dx", "-0.8em")
    .attr("dy", "0.15em")
    .style("text-anchor", "end")
    .style("font-size", "11px")
    .style("fill", "#F9E8DE");

    svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).tickFormat(d => `${(d * 100).toFixed(0)}%`))
    .selectAll("text")
    .style("fill", "#F9E8DE");

  // --- BARS ---
  const groups = svg.selectAll(".group")
    .data(top10)
    .enter()
    .append("g")
    .attr("class", "group")
    .attr("transform", d => `translate(${x0(d.CBSA_Name)},0)`);

  groups.selectAll("rect")
    .data(d => [
      { key: "LoWgWrks", value: d.pct_LoWgWrks_byTr },
      { key: "MeWgWrks", value: d.pct_MeWgWrks_byTr }
    ])
    .enter()
    .append("rect")
    .attr("x", d => x1(d.key))
    .attr("y", d => y(d.value))
    .attr("width", x1.bandwidth())
    .attr("height", d => y(0) - y(d.value))
    .attr("fill", d => color(d.key));

  // --- TITLE ---
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", 30)
    .attr("text-anchor", "middle")
    .style("font-size", "18px")
    .style("font-weight", "bold")
    .text("Top 10 Metro Areas: Largest Transit Access Disparities by Wage")
    .style("fill", "#F9E8DE");

  // --- AXIS LABELS ---
  svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("y", 25)
    .attr("text-anchor", "middle")
    .style("font-size", "14px")
    .text("Avg. % of Jobs Reachable (≤ 45 min)")
    .style("fill", "#F9E8DE");

  // --- LEGEND ---
  const legend = svg.append("g")
    .attr("transform", `translate(${margin.left + 10}, 60)`);  // Position it at the left side, near the top

  const categories = [
    { key: "LoWgWrks", label: "Low-Wage Workers (≤ $1250/month)" },
    { key: "MeWgWrks", label: "Medium-Wage Workers (Between $1250/month and $3333/month)" }
  ];

  categories.forEach((cat, i) => {
    legend.append("rect")
      .attr("x", 0)
      .attr("y", i * 25)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color(cat.key));

    legend.append("text")
      .attr("x", 25)
      .attr("y", i * 25 + 13)
      .text(cat.label)
      .style("font-size", "13px")
      .style("fill", "#F9E8DE");;
  });
});