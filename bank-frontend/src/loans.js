let currentPage = 1;
const pageSize = 15;
let totalLoans = 0;

document.addEventListener("DOMContentLoaded", () => {
    fetchLoans();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById("apply-loan-filters").addEventListener("click", () => {
        currentPage = 1;
        fetchLoans(); // This will pull values from the DOM inside fetchLoans()
    });

    // Optional: remove these if you only want filtering on button click
    // document.getElementById("search-loan-status").addEventListener("input", fetchLoans);
    // document.getElementById("search-loan-type").addEventListener("input", fetchLoans);
    // document.getElementById("interest-rate").addEventListener("change", fetchLoans);
    // document.getElementById("sort-order").addEventListener("change", fetchLoans);
    // document.getElementById("sort-direction").addEventListener("change", fetchLoans);
}


function toggleLoanForm() {
    const form = document.getElementById("add-loan-form");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

function fetchLoans() {
    const type = document.getElementById("search-loan-type").value.trim();
    const status = document.getElementById("search-loan-status").value.trim();
    const rate = document.getElementById("interest-rate").value;
    const sortBy = document.getElementById("sort-order").value;
    const sortDir = document.getElementById("sort-direction").value;

    const url = new URL("http://localhost:8000/loans");
    url.searchParams.append("page", currentPage);
    url.searchParams.append("page_size", pageSize);

    if (type) url.searchParams.append("loan_type", type);
    if (status) url.searchParams.append("status", status);

    if (rate === "high") url.searchParams.append("min_interest_rate", "10");
    else if (rate === "low") url.searchParams.append("max_interest_rate", "10");

    if (sortBy) {
        url.searchParams.append("sort_by", sortBy);
        url.searchParams.append("sort_order", sortDir || "asc");
    }

    const tableBody = document.getElementById("loans-table-body");
    if (tableBody) {
        tableBody.innerHTML = `<tr><td colspan="9">Loading loans...</td></tr>`;
    }

    fetch(url)
        .then(res => res.json())
        .then(data => {
            totalLoans = data.total_count;
            renderLoans(data.loans);
            renderPaginationControls();
        })
        .catch(err => {
            console.error("Error fetching loans:", err);
            if (tableBody) {
                tableBody.innerHTML = `<tr><td colspan="9" style="color: red;">Failed to load loans.</td></tr>`;
            }
        });
}

function renderLoans(loans) {
    const tableBody = document.getElementById("loans-table-body");
    tableBody.innerHTML = "";

    if (!loans || loans.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="9">No loans found</td>`;
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
        `;
        tableBody.appendChild(row);
    });
}

function renderPaginationControls() {
    const container = document.getElementById("pagination-controls");
    if (!container) return;
    container.innerHTML = "";

    const totalPages = Math.ceil(totalLoans / pageSize);
    if (totalPages <= 1) return;

    if (currentPage > 1) {
        const prevBtn = document.createElement("button");
        prevBtn.textContent = "←";
        prevBtn.onclick = () => {
            currentPage--;
            fetchLoans();
        };
        container.appendChild(prevBtn);
    }

    for (let i = 1; i <= totalPages; i++) {
        const pageBtn = document.createElement("button");
        pageBtn.textContent = i;
        if (i === currentPage) {
            pageBtn.disabled = true;
            pageBtn.style.fontWeight = "bold";
        }
        pageBtn.onclick = () => {
            currentPage = i;
            fetchLoans();
        };
        container.appendChild(pageBtn);
    }

    if (currentPage < totalPages) {
        const nextBtn = document.createElement("button");
        nextBtn.textContent = "→";
        nextBtn.onclick = () => {
            currentPage++;
            fetchLoans();
        };
        container.appendChild(nextBtn);
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

function submitLoanForm(e) {
    e.preventDefault();

    const newLoan = {
        type: document.getElementById("new-loan-type").value,
        open_date: document.getElementById("new-loan-open-date").value,
        term_length: parseInt(document.getElementById("new-loan-term-length").value),
        amount: parseFloat(document.getElementById("new-loan-amount").value),
        status: document.getElementById("new-loan-status").value,
        interest_rate: parseFloat(document.getElementById("new-loan-interest-rate").value),
        fk_person_id: parseInt(document.getElementById("new-loan-person-id").value),
        fk_bank_id: parseInt(document.getElementById("new-loan-bank-id").value)
    };

    fetch("http://localhost:8000/loans", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newLoan)
    })
        .then(res => res.json())
        .then(() => {
            alert("Loan added successfully!");
            clearLoanForm();
            fetchLoans();
        })
        .catch(err => {
            console.error("Failed to insert loan:", err);
            alert("Failed to insert loan.");
        });
}

function clearLoanForm() {
    document.getElementById("add-loan-form").reset();
}
