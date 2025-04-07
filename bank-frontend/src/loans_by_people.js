// loans_by_people.js
let currentPage = 1;
const pageSize = 15;
let totalPages = 1;

const personFilterState = {
    firstName: "",
    lastName: "",
    address: "",
    status: "",
    loanType: "",
    interestRateFilter: "",
    sortBy: "",
    sortOrder: ""
};

document.addEventListener("DOMContentLoaded", () => {
    fetchLoansByPerson();
    setupPersonEventListeners();
});

function setupPersonEventListeners() {
    const applyButton = document.getElementById("apply-loan-filters");

    applyButton.addEventListener("click", () => {
        personFilterState.firstName = document.getElementById("search-person-first-name").value.trim();
        personFilterState.lastName = document.getElementById("search-person-last-name").value.trim();    
        personFilterState.status = document.getElementById("search-loan-status").value.trim();
        personFilterState.loanType = document.getElementById("search-loan-type").value.trim();
        personFilterState.interestRateFilter = document.getElementById("interest-rate").value;
        personFilterState.sortBy = document.getElementById("sort-order").value;
        personFilterState.sortOrder = document.getElementById("sort-direction").value;

        currentPage = 1;
        fetchLoansByPerson();
    });
}

function fetchLoansByPerson() {
    const url = new URL("http://localhost:8000/loans");

    url.searchParams.append("page", currentPage);
    url.searchParams.append("page_size", pageSize);
    if (personFilterState.firstName) {
        url.searchParams.append("first_name", personFilterState.firstName);
      }
      if (personFilterState.lastName) {
        url.searchParams.append("last_name", personFilterState.lastName);
      }
      
    if (personFilterState.status) url.searchParams.append("status", personFilterState.status);
    if (personFilterState.loanType) url.searchParams.append("loan_type", personFilterState.loanType);

    if (personFilterState.interestRateFilter === "high") {
        url.searchParams.append("min_interest_rate", "10");
    } else if (personFilterState.interestRateFilter === "low") {
        url.searchParams.append("max_interest_rate", "10");
    }

    if (personFilterState.sortBy) {
        url.searchParams.append("sort_by", personFilterState.sortBy);
        url.searchParams.append("sort_order", personFilterState.sortOrder || "asc");
    }

    fetch(url)
        .then(res => res.json())
        .then(data => {
            renderLoansWithPersonTable(data.loans);
            renderPaginationControls(data.total_count);
        })
        .catch(err => {
            console.error("Error fetching loans by person:", err);
            alert("Failed to fetch loans.");
        });
}

function renderLoansWithPersonTable(loans) {
    const tableBody = document.getElementById("loans-table-with-person-join-body");
    tableBody.innerHTML = "";

    if (!loans || loans.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="17">No loans found</td>`;
        tableBody.appendChild(row);
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
            <td>${loan.first_name}</td>
            <td>${loan.last_name}</td>
            <td>${loan.birthday}</td>
            <td>${loan.email}</td>
            <td>${loan.phone_number}</td>
            <td>${loan.address}</td>
            <td>${loan.ssn}</td>
            <td>${loan.credit_score}</td>
        `;
        tableBody.appendChild(row);
    });
}

function renderPaginationControls(totalCount) {
    const container = document.getElementById("pagination-controls");
    container.innerHTML = "";

    totalPages = Math.ceil(totalCount / pageSize);
    if (totalPages <= 1) return;

    if (currentPage > 1) {
        const prev = document.createElement("button");
        prev.textContent = "←";
        prev.onclick = () => {
            currentPage--;
            fetchLoansByPerson();
        };
        container.appendChild(prev);
    }

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
            fetchLoansByPerson();
        });
        container.appendChild(pageBtn);
    }

    if (currentPage < totalPages) {
        const next = document.createElement("button");
        next.textContent = "→";
        next.onclick = () => {
            currentPage++;
            fetchLoansByPerson();
        };
        container.appendChild(next);
    }
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
