const transitData = d3.csv("outputs/metro_aggregated.csv");

transitData.then(function(data) {
  // Convert string values to numbers and calculate difference
  data.forEach(d => {
    d.avg_LoWgWrks_byTr = +d.avg_LoWgWrks_byTr;
    d.avg_HiWgWrks_byTr = +d.avg_HiWgWrks_byTr;
    d.Diff = Math.abs(d.avg_LoWgWrks_byTr - d.avg_HiWgWrks_byTr);
  });

  // Filter out rows with missing data
  const validData = data.filter(d => 
    !isNaN(d.avg_LoWgWrks_byTr) && 
    !isNaN(d.avg_HiWgWrks_byTr) &&
    d.avg_LoWgWrks_byTr > 0 &&
    d.avg_HiWgWrks_byTr > 0
  );

  // Sort by difference and get top 10
  validData.sort((a, b) => b.Diff - a.Diff);
  const top10 = validData.slice(0, 10);

  console.log("Top 10 CBSAs:", top10.map(d => ({ name: d.CBSA_Name, diff: d.Diff })));

  // --- SVG setup ---
  const width = 600, height = 900;
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
    .domain(["LoWgWrks", "HiWgWrks"])
    .range([0, x0.bandwidth()])
    .padding(0.1);

  const y = d3.scaleLinear()
    .domain([0, d3.max(top10, d => Math.max(d.avg_LoWgWrks_byTr, d.avg_HiWgWrks_byTr))])
    .nice()
    .range([height - margin.bottom, margin.top]);

  const color = d3.scaleOrdinal()
    .domain(["LoWgWrks", "HiWgWrks"])
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
    .style("fill", "#FFFFFF");

  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).tickFormat(d3.format(".2s")))
    .selectAll("text")
    .style("fill", "#FFFFFF");

  // --- BARS ---
  const groups = svg.selectAll(".group")
    .data(top10)
    .enter()
    .append("g")
    .attr("class", "group")
    .attr("transform", d => `translate(${x0(d.CBSA_Name)},0)`);

  groups.selectAll("rect")
    .data(d => [
      { key: "LoWgWrks", value: d.avg_LoWgWrks_byTr },
      { key: "HiWgWrks", value: d.avg_HiWgWrks_byTr }
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
    .style("fill", "#FFFFFF");

  // --- AXIS LABELS ---
  svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("y", 25)
    .attr("text-anchor", "middle")
    .style("font-size", "14px")
    .text("Avg. Workers Reachable in 45 min")
    .style("fill", "#FFFFFF");

  // --- LEGEND ---
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 320}, ${margin.top + 20})`);

  const categories = [
    { key: "LoWgWrks", label: "Low-Wage Workers (≤ $1250/month)" },
    { key: "HiWgWrks", label: "High-Wage Workers (> $3333/month)" }
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
      .style("fill", "#FFFFFF");;
  });
});