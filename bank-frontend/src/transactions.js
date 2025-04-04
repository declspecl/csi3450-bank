document.addEventListener("DOMContentLoaded", fetchTransactions);

function fetchTransactions() {
    fetch('http://localhost:8000/transactions')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("transactionTableBody");
            tableBody.innerHTML = "";
            data.transactions.forEach(tx => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${tx.sender}</td>
                    <td>${tx.recipient}</td>
                    <td>${tx.status}</td>
                    <td>$${tx.amount}</td>
                    <td>${tx.date}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error fetching transactions:", error);
            alert("Failed to fetch transactions");
        });
}