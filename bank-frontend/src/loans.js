let currentPage = 1;
const pageSize = 15;
let totalLoans = 0;

const filterState = {
    status: "",
    loanType: "",
    interestRateFilter: "",
    sortAmount: "",
    bankName: "",
    personName: ""
};

document.addEventListener("DOMContentLoaded", () => {
    fetchLoans();
    setupEventListeners();
});

function setupEventListeners() {
    const statusSelectors = document.querySelectorAll('.status-filter');
    const loanTypeSelectors = document.querySelectorAll('.loan-type-filter');
    const interestRateSelectors = document.querySelectorAll('.interest-rate-filter');
    const sortAmountSelectors = document.querySelectorAll('.sort-amount');
    const searchButtons = document.querySelectorAll('.search-button');
    
    statusSelectors.forEach(selector => {
        selector.addEventListener('change', function() {
            filterState.status = this.value;
            syncFilters('status', this.value);
        });
    });
    
    loanTypeSelectors.forEach(selector => {
        selector.addEventListener('change', function() {
            filterState.loanType = this.value;
            syncFilters('loanType', this.value);
        });
    });
    
    interestRateSelectors.forEach(selector => {
        selector.addEventListener('change', function() {
            filterState.interestRateFilter = this.value;
            syncFilters('interestRateFilter', this.value);
        });
    });
    
    sortAmountSelectors.forEach(selector => {
        selector.addEventListener('change', function() {
            filterState.sortAmount = this.value;
            syncFilters('sortAmount', this.value);
        });
    });
    
    const bankNameInput = document.getElementById('bank-name-input');
    if (bankNameInput) {
        bankNameInput.addEventListener('input', function() {
            filterState.bankName = this.value;
        });
    }
    
    const personNameInput = document.getElementById('person-name-input');
    if (personNameInput) {
        personNameInput.addEventListener('input', function() {
            filterState.personName = this.value;
        });
    }
    
    searchButtons.forEach(button => {
        button.addEventListener('click', applyFilters);
    });
    
    const addLoanForm = document.getElementById("add-loan-form");
    if (addLoanForm) {
        addLoanForm.addEventListener("submit", submitNewLoan);
    }
}

function syncFilters(filterType, value) {
    let selectorClass = '';
    
    switch(filterType) {
        case 'status':
            selectorClass = '.status-filter';
            break;
        case 'loanType':
            selectorClass = '.loan-type-filter';
            break;
        case 'interestRateFilter':
            selectorClass = '.interest-rate-filter';
            break;
        case 'sortAmount':
            selectorClass = '.sort-amount';
            break;
    }
    
    if (selectorClass) {
        document.querySelectorAll(selectorClass).forEach(selector => {
            selector.value = value;
        });
    }
}

function applyFilters() {
    currentPage = 1;
    fetchLoans();
}

function fetchLoans() {
    const url = new URL("http://localhost:8000/loans");
    
    if (filterState.status) url.searchParams.append("status", filterState.status);
    if (filterState.loanType) url.searchParams.append("loan_type", filterState.loanType);
    
    if (filterState.interestRateFilter === "high") {
        url.searchParams.append("min_interest_rate", "10");
    } else if (filterState.interestRateFilter === "low") {
        url.searchParams.append("max_interest_rate", "10");
    }
    
    if (filterState.sortAmount) {
        url.searchParams.append("sort_by_amount", "true");
        url.searchParams.append("sort_order", filterState.sortAmount);
    }
    
    if (filterState.bankName) url.searchParams.append("bank_name", filterState.bankName);
    if (filterState.personName) url.searchParams.append("name", filterState.personName);
    
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
            <td>${loan.open_date}</td>
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
            <td>${loan.open_date}</td>
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
            <td>${loan.open_date}</td>
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
