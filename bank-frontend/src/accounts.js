function fetchAccounts() {
    const name = document.getElementById("filterName").value;
    const accountType = document.getElementById("filterType").value;
    const status = document.getElementById("filterStatus").value;

    let url = `http://localhost:8000/accounts`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("accountTableBody");
            tableBody.innerHTML = "";
            data.accounts.forEach(account => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${account.account_number}</td>
                    <td>${account.routing_number}</td>
                    <td>${account.account_type}</td>
                    <td>$${account.balance}</td>
                    <td>${account.status}</td>
                    <td>${account.fk_person_id}</td>
                    <td>${account.fk_bank_id}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error fetching accounts:", error);
            alert("Failed to fetch accounts");
        });
        fetchAccounts();
}