const columns = [
    { name: "state", description: "Name of the U.S. state" },
    { name: "unemployment_rate", description: "Percentage of people unemployed in the labor force" },
    { name: "transit_access", description: "Level of public transit accessibility within the state" },
    { name: "median_income", description: "Median household income in USD" }
];

const container = document.getElementById("column-table");

// Create header row
const header = document.createElement("div");
header.classList.add("row", "header");
header.innerHTML = `
    <div class="cell">Column Name</div>
    <div class="cell">Description</div>
`;
container.appendChild(header);

// Create rows dynamically
columns.forEach(col => {
    const row = document.createElement("div");
    row.classList.add("row");
    row.innerHTML = `
        <div class="cell">${col.name}</div>
        <div class="cell">${col.description}</div>
    `;
    container.appendChild(row);
});