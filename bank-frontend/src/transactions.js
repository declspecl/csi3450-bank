document.addEventListener("DOMContentLoaded", () => {
    fetchTransactions();
});

function fetchTransactions() {
    const sortBy = document.getElementById("sortBy").value;
    const filterStatus = document.getElementById("filterStatus").value;

    const url = new URL("http://localhost:8000/transactions");
    url.searchParams.set("sort_by_amount", sortBy === "amount" ? true : false);
    url.searchParams.set("recent", sortBy === "date" ? true : false);
    url.searchParams.set("status", filterStatus);

    fetch(url)
        .then(response => response.json())
        .then(data => {
            allTransactions = data.transactions;
            renderTransactions(allTransactions);
        })
        .catch(error => {
            console.error("Error fetching transactions:", error);
            alert("Failed to fetch transactions");
        });
}

function renderTransactions(transactions) {
    const tableBody = document.getElementById("transactionTableBody");
    tableBody.innerHTML = "";
    
    if (transactions.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="5">No transactions found</td>`;
        tableBody.appendChild(row);
        return;
    }
    
    transactions.forEach(tx => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${tx.transaction_id}</td>
            <td>$${tx.amount}</td>
            <td>${tx.fk_sender_id}</td>
            <td>${tx.fk_recipient_id}</td>
            <td>${tx.status}</td>
            <td>${tx.transaction_date}</td>
        `;
        tableBody.appendChild(row);
    });
}