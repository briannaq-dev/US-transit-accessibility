// Reusable function to create a table
function createTable(columns, containerId) {
    const container = document.getElementById(containerId);
    
    // Create header row
    const header = document.createElement("div");
    header.classList.add("row", "header");
    header.innerHTML = `
        <div class="cell">Column Name</div>
        <div class="cell">Description</div>
    `;
    container.appendChild(header);
    
    // Create rows
    columns.forEach(col => {
        const row = document.createElement("div");
        row.classList.add("row");
        row.innerHTML = `
            <div class="cell">${col.name}</div>
            <div class="cell">${col.description}</div>
        `;
        container.appendChild(row);
    });
}

// First table data
const smartLocationColumns = [
    { name: "CBSA_Name", description: "Name of the core based statistical area (or metropolitan region) in which block group resides." },
    { name: "TrAccess_Index", description: "An index of relative accessibility compared to other block groups within the same metro region, as measured by travel time to working-age population via transit." },
    { name: "Pct_Jobs_byTr_av", description: "Percentage of jobs reachable within a 45-minute transit and walking commute" },
    { name: "pct_LoWgWrks_byTr", description: "Percentage of low-wage workers able to reach their jobs within a 45-minute transit and walking commute" },
    { name: "pct_MeWgWrks_byTr", description: "Percentage of medium-wage workers able to reach their jobs within a 45-minute transit and walking commute" }
];

// Second table data
const sldTransColumns = [
    { name: "CBSA_POP", description: "Population size" },
    { name: "D1B", description: "Population Density (People/Acre)" },
    { name: "NatWalkInd", description: "Walkability Index Score (0-20)" },
    { name: "Pct_AO0", description: "Percent of zero-car households" }
];

// Create both tables
createTable(smartLocationColumns, "column-table");
createTable(sldTransColumns, "column-table-2");