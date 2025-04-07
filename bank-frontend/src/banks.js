document.addEventListener("DOMContentLoaded", () => {
    fetchBanks(); // Fetch banks on page load
    setupEventListeners();
});

function setupEventListeners() {
    // Apply filters on button click
    document.getElementById("apply-bank-filters").addEventListener("click", () => {
        fetchBanks(); // Fetch banks when filters are applied
    });

    // Toggle form visibility
    document.getElementById("toggle-insert-form").addEventListener("click", () => {
        const form = document.getElementById("add-bank-form");
        form.style.display = form.style.display === "none" ? "block" : "none";
    });
}

function fetchBanks() {
    const bankName = document.getElementById("bank-name-input").value.trim();
    const bankLocation = document.getElementById("bank-location-input").value.trim();
    const sortBy = document.getElementById("sort-order").value;
    const sortDirection = document.getElementById("sort-direction").value;

    const url = new URL("http://localhost:8000/banks");  // Update with your API URL

    // Append the filters to the URL
    if (bankName) url.searchParams.append("name", bankName);
    if (bankLocation) url.searchParams.append("location", bankLocation);
    if (sortBy) url.searchParams.append("sort_by", sortBy);
    if (sortDirection) url.searchParams.append("sort_direction", sortDirection);

    // Show loading message while fetching data
    const tableBody = document.getElementById("banks-table-body");
    if (tableBody) {
        tableBody.innerHTML = `<tr><td colspan="5">Loading banks...</td></tr>`;
    }

    // Fetch the data from the API
    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderBanks(data.banks);  // Render the filtered banks
        })
        .catch(err => {
            console.error("Error fetching banks:", err);
            if (tableBody) {
                tableBody.innerHTML = `<tr><td colspan="5" style="color: red;">Failed to load banks.</td></tr>`;
            }
        });
}

function renderBanks(banks) {
    const tableBody = document.getElementById("banks-table-body");
    tableBody.innerHTML = "";

    if (!banks || banks.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="5">No banks found</td>`;
        tableBody.appendChild(row);
        return;
    }

    banks.forEach(bank => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${bank.bank_id}</td>
            <td>${bank.name}</td>
            <td>${bank.routing_number}</td>
            <td>${bank.location}</td>
            <td>${bank.phone_number}</td>
        `;
        tableBody.appendChild(row);
    });
}
