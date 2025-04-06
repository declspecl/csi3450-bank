// Global variables for pagination
let currentPage = 1;
const pageSize = 15;
let totalLoans = 0;

document.addEventListener("DOMContentLoaded", () => {
    fetchLoans();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById("search-button").addEventListener("click", applyFilters);
    
    const addLoanForm = document.getElementById("add-loan-form");
    if (addLoanForm) {
        addLoanForm.addEventListener("submit", submitNewLoan);
    }
}

function applyFilters() {
    currentPage = 1;
    fetchLoans();
}

function fetchLoans() {
    const status = document.getElementById("status-filter").value;
    const loanType = document.getElementById("loan-type-filter").value;
    const interestRateFilter = document.getElementById("interest-rate-filter").value;
    const sortAmount = document.getElementById("sort-amount").value;
    
    const url = new URL("http://localhost:8000/loans");
    
    if (status) url.searchParams.append("status", status);
    if (loanType) url.searchParams.append("loan_type", loanType);
    
    if (interestRateFilter === "high") {
        url.searchParams.append("min_interest_rate", "10");
    } else if (interestRateFilter === "low") {
        url.searchParams.append("max_interest_rate", "10");
    }
    
    if (sortAmount) {
        url.searchParams.append("sort_by_amount", "true");
        url.searchParams.append("sort_order", sortAmount);
    }
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch loans");
            }
            return response.json();
        })
        .then(data => {
            renderLoansTable(data.loans);
            renderLoansWithBankTable(data.loans);
            renderLoansWithPersonTable(data.loans);
        })
        .catch(error => {
            console.error("Error fetching loans:", error);
            alert("Failed to fetch loans");
        });
}

function renderLoansTable(loans) {
    const tableBody = document.getElementById("loans-table-body");
    tableBody.innerHTML = "";
    
    if (!loans || loans.length === 0) {
        const noDataRow = document.createElement("tr");
        noDataRow.innerHTML = `<td colspan="9">No loans found</td>`;
        tableBody.appendChild(noDataRow);
        return;
    }
    
    loans.forEach(loan => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${loan.loan_id}</td>
            <td>${loan.type}</td>
            <td>${loan.open_date || 'N/A'}</td>
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
            <td>${loan.open_date || 'N/A'}</td>
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

function renderLoansWithPersonTable(loans) {
    const tableBody = document.getElementById("loans-table-with-person-join-body");
    tableBody.innerHTML = "";
    
    if (!loans || loans.length === 0) {
        const noDataRow = document.createElement("tr");
        noDataRow.innerHTML = `<td colspan="17">No loans found</td>`;
        tableBody.appendChild(noDataRow);
        return;
    }
    
    loans.forEach(loan => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${loan.loan_id}</td>
            <td>${loan.type}</td>
            <td>${loan.open_date || 'N/A'}</td>
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

function submitNewLoan(event) {
    event.preventDefault();
    
    const loanType = document.getElementById("new-loan-type").value;
    const openDate = document.getElementById("new-loan-open-date").value;
    const termLength = document.getElementById("new-loan-term-length").value;
    const amount = document.getElementById("new-loan-amount").value;
    const status = document.getElementById("new-loan-status").value;
    const interestRate = document.getElementById("new-loan-interest-rate").value;
    const personId = document.getElementById("new-loan-person-id").value;
    const bankId = document.getElementById("new-loan-bank-id").value;
    
    if (!loanType || !openDate || !termLength || !amount || !status || !interestRate || !personId || !bankId) {
        alert("Please fill in all fields.");
        return;
    }
    
    const newLoan = {
        type: loanType,
        open_date: openDate,
        term_length: parseInt(termLength),
        amount: parseFloat(amount),
        status: status,
        interest_rate: parseFloat(interestRate),
        fk_person_id: parseInt(personId),
        fk_bank_id: parseInt(bankId)
    };
    
    fetch("http://localhost:8000/loans", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newLoan)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to add loan");
        }
        return response.json();
    })
    .then(() => {
        alert("Loan added successfully!");
        clearLoanForm();
        fetchLoans();
    })
    .catch(error => {
        console.error("Error adding loan:", error);
        alert("Failed to add loan: " + error.message);
    });
}

function clearLoanForm() {
    document.getElementById("new-loan-type").value = "";
    document.getElementById("new-loan-open-date").value = "";
    document.getElementById("new-loan-term-length").value = "";
    document.getElementById("new-loan-amount").value = "";
    document.getElementById("new-loan-status").value = "";
    document.getElementById("new-loan-interest-rate").value = "";
    document.getElementById("new-loan-person-id").value = "";
    document.getElementById("new-loan-bank-id").value = "";
}
