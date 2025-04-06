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

// Toggle form visibility
function toggleForm() {
    const form = document.getElementById("new-transaction-form");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

// Clear the transaction form
function clearTransactionForm() {
    document.getElementById("amount").value = "";
    document.getElementById("transaction-date").value = "";
    document.getElementById("status").value = "";
    document.getElementById("sender-id").value = "";
    document.getElementById("recipient-id").value = "";
}

// Display confirmation message
function showConfirmationMessage() {
    const msg = document.createElement('p');
    msg.textContent = "✅ Transaction submitted! Your money is now in digital limbo.";
    msg.style.color = "gold";
    msg.style.fontWeight = "bold";
    msg.style.marginTop = "10px";
    msg.style.textShadow = "1px 1px 2px black";
    
    document.getElementById("new-transaction-form").appendChild(msg);
    
    setTimeout(() => {
        msg.remove();
    }, 5000); // disappears after 5 seconds
}

// Submit new transaction to server
function submitNewTransaction() {
    const amount = document.getElementById("amount").value;
    const transactionDate = document.getElementById("transaction-date").value;
    const status = document.getElementById("status").value;
    const senderId = document.getElementById("sender-id").value;
    const recipientId = document.getElementById("recipient-id").value;

    // Validate input
    if (!amount || !transactionDate || !status || !senderId || !recipientId) {
        alert("Please fill in all fields.");
        return;
    }

    // Create transaction object
    const newTransaction = {
        amount: parseFloat(amount),
        transaction_date: transactionDate,
        status: status,
        fk_sender_id: parseInt(senderId),
        fk_recipient_id: parseInt(recipientId)
    };

    // Submit transaction to server
    fetch("http://localhost:8000/transactions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(newTransaction),
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed to add new transaction");
        return res.json();
    })
    .then(() => {
        showConfirmationMessage();
        fetchTransactions();
        clearTransactionForm();
    })
    .catch(err => {
        alert("Error: " + err.message);
    });
}