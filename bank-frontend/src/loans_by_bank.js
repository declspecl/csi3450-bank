let currentPage = 1;
const pageSize = 15;
let totalPages = 1; // Total number of pages for pagination

const bankFilterState = {
    status: "",
    loanType: "",
    interestRateFilter: "",
    sortAmount: "",
    bankName: "",
    bankName: "",
    bankLocation: "",
    bankPhone: ""

};
document.addEventListener("DOMContentLoaded", () => {
    fetchLoansByBank();
    setupBankEventListeners();
});

function setupBankEventListeners() {
    const searchButton = document.getElementById('apply-loan-filters');

    if (searchButton) {
        searchButton.addEventListener('click', () => {
            bankFilterState.status = document.getElementById('search-loan-status')?.value.trim() || "";
            bankFilterState.loanType = document.getElementById('search-loan-type')?.value.trim() || "";
            bankFilterState.interestRateFilter = document.getElementById('interest-rate')?.value || "";
            bankFilterState.sortAmount = document.getElementById('sort-order')?.value || "";
            bankFilterState.sortDirection = document.getElementById('sort-direction')?.value || "";

            
            bankFilterState.bankLocation = document.getElementById('search-bank-location')?.value.trim() || "";
            bankFilterState.bankPhone = document.getElementById('search-bank-phone')?.value.trim() || "";

            fetchLoansByBank();
        });
    }
}





function syncFilters(filterType, value) {
    let selectorClass = '';
    switch (filterType) {
        case 'status':
            selectorClass = '.status-filter'; break;
        case 'loanType':
            selectorClass = '.loan-type-filter'; break;
        case 'interestRateFilter':
            selectorClass = '.interest-rate-filter'; break;
        case 'sortAmount':
            selectorClass = '.sort-amount'; break;
    }
    if (selectorClass) {
        document.querySelectorAll(selectorClass).forEach(selector => {
            selector.value = value;
        });
    }
}
function fetchLoansByBank() {
    const url = new URL("http://localhost:8000/loans");
    url.searchParams.append("join", "bank");
    url.searchParams.append("page", currentPage); // 👈 Add this
    url.searchParams.append("page_size", pageSize); // 👈 And this

    if (bankFilterState.status) url.searchParams.append("status", bankFilterState.status);
    if (bankFilterState.loanType) url.searchParams.append("loan_type", bankFilterState.loanType);
    if (bankFilterState.bankLocation) url.searchParams.append("bank_location", bankFilterState.bankLocation);
    if (bankFilterState.bankPhone) url.searchParams.append("bank_phone", bankFilterState.bankPhone);

    if (bankFilterState.interestRateFilter === "high") {
        url.searchParams.append("min_interest_rate", "10");
    } else if (bankFilterState.interestRateFilter === "low") {
        url.searchParams.append("max_interest_rate", "10");
    }

    if (bankFilterState.sortAmount) {
        url.searchParams.append("sort_by", bankFilterState.sortAmount);
        url.searchParams.append("sort_order", bankFilterState.sortDirection || "asc");
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderLoansWithBankTable(data.loans);
            renderPaginationControls(data.total_count); // 👈 Add pagination rendering
        })
        .catch(err => {
            console.error("Error fetching loans by bank:", err);
            alert("Failed to fetch loans.");
        });
}



function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString(undefined, {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric"
    });
}

function renderLoansWithBankTable(loans) {
    const tableBody = document.getElementById("loans-table-with-bank-join-body");
    tableBody.innerHTML = "";

    if (!loans || loans.length === 0) {
        const noDataRow = document.createElement("tr");
        noDataRow.innerHTML = `<td colspan="13">No loans found</td>`;
        tableBody.appendChild(noDataRow);
        return;
    }

    loans.forEach(loan => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${loan.loan_id}</td>
            <td>${loan.type}</td>
            <td>${formatDate(loan.open_date)}</td>
            <td>${loan.term_length}</td>
            <td>$${parseFloat(loan.amount).toFixed(2)}</td>
            <td>${loan.status}</td>
            <td>${parseFloat(loan.interest_rate).toFixed(2)}%</td>
            <td>${loan.fk_person_id}</td>
            <td>${loan.fk_bank_id}</td>
            <td>${loan.bank_name}</td>
            <td>${loan.bank_routing_number}</td>
            <td>${loan.bank_location}</td>
            <td>${loan.bank_phone_number}</td>
        `;
        tableBody.appendChild(row);
    });
}

function renderPaginationControls(totalCount) {
    const container = document.getElementById("pagination-controls");
    container.innerHTML = "";

    totalPages = Math.ceil(totalCount / pageSize);

    if (totalPages <= 1) return;

    // Previous button
    if (currentPage > 1) {
        const prev = document.createElement("button");
        prev.textContent = "←";
        prev.onclick = () => {
            currentPage--;
            fetchLoansByBank();
        };
        container.appendChild(prev);
    }

    // Numbered page buttons
    for (let i = 1; i <= totalPages; i++) {
        const pageBtn = document.createElement("button");
        pageBtn.textContent = i;
        pageBtn.style.margin = "0 3px";
        if (i === currentPage) {
            pageBtn.style.fontWeight = "bold";
            pageBtn.disabled = true;
        }
        pageBtn.addEventListener("click", () => {
            currentPage = i;
            fetchLoansByBank();
        });
        container.appendChild(pageBtn);
    }

    // Next button
    if (currentPage < totalPages) {
        const next = document.createElement("button");
        next.textContent = "→";
        next.onclick = () => {
            currentPage++;
            fetchLoansByBank();
        };
        container.appendChild(next);
    }
}

