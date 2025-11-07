const columns = [
    { name: "CBSA_Name", description: "Name of the core based statistical area (or metropolitan region) in which block group resides." },
    { name: "TrAccess_Index", description: "An index of relative accessibilitycompared to other block groups within the same metro region, as measured by travel time to working-age population via transit." },
    { name: "Pop_byTr", description: "Total population able to access the block group within a 45-minute transit and walking commute" },
    { name: "Pop_byTr_min", description: "Minimum Pop_byTr among all block groups within same CBSA" }
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