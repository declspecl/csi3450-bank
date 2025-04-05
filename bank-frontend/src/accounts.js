//  Shoutout to Nicholas for the code
// I am resetting this to work with pagination
// function to fetch account data from the server
// function to render the account table
// function to render pagination controls
// you will need to update backend to support pagination
// and sorting

//constraints for pagination
let currentPage = 1;
const itemsPerPage = 15; // Number of items per page
let totalPages = 1; // This should be dynamically set based on the total number of items

//function to fetch account data from the server
function fetchAccounts() {
    const personID = document.getElementById("search-person-ID").value;
    const accountType = document.getElementById("search-account-type").value;
    const status = document.getElementById("search-account-status").value;
    const sortBy = document.getElementById("sort-by").value;
    const sortOrder = document.getElementById("sort-order").value;

    let query = `?page=${currentPage}&page_size=${itemsPerPage}`;

    if (personID) query += `&fk_person_id=${encodeURIComponent(personID)}`;
    if (accountType) query += `&account_type=${encodeURIComponent(accountType)}`;
    if (status) query += `&status=${encodeURIComponent(status)}`;
    if (sortBy) query += `&sort_by=${sortBy}&sort_order=${sortOrder}`;

    fetch(`http://localhost:8000/accounts${query}`)
        .then(res => {
            if (!res.ok) throw new Error("Failed to fetch accounts");
            return res.json();
        })
        .then(data => {
            renderAccountsTable(data.accounts);

            // Setting totalPages based on the response from backend if it has total_count of accounts
            if (data.total_count !== undefined) {
                totalPages = Math.ceil(data.total_count / itemsPerPage);
                renderPagination();
            }
        })
        .catch(err => {
            document.getElementById('account-table-container').innerHTML =
              `<p style="color:red;">Error loading accounts: ${err.message}</p>`;
          });
}


//render the account table
function renderAccountsTable(accounts) {
    const container = document.getElementById('account-table-container');
    container.innerHTML = '';

    const table = document.createElement('table');
    const headers = ['#','Account Number', 'Routing Number', 'Account Type', 'Balance', 'Status', 'Person ID', 'Bank Name'];
    const headerRow = document.createElement('tr');

    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    accounts.forEach((account, index) => {
        const row = document.createElement('tr');

        //adding an entry number to the table
        //will increment data as i dont think we want to show account ID?
        const entryNumber = (currentPage - 1) * itemsPerPage + index +1; //shows actual position

        const cells = [
            entryNumber, // Entry number    
            account.account_number,
            account.routing_number,
            account.account_type,
            `$${parseFloat(account.balance).toFixed(2)}`,
            account.status,
            account.fk_person_id,
            account.bank_name  // changed from fk_bank_id to bank_name
        ];

        cells.forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            row.appendChild(td);
        });

        table.appendChild(row);
    });

    container.appendChild(table);
}


//function to render pagination controls
function renderPagination() {
    const container = document.getElementById('pagination-controls');
    container.innerHTML = '';
  
    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement('button');
      btn.textContent = i;
      btn.style.margin = '0 5px';
      btn.onclick = () => {
        currentPage = i;
        fetchAccounts();
      };
  
      if (i === currentPage) {
        btn.style.fontWeight = 'bold';
        btn.style.backgroundColor = '#C5A30F';
        btn.style.color = '#000';
      }
  
      container.appendChild(btn);
    }
  }

  //fucntion for sorting functionality with pagination
  function applyFilters() {
    currentPage = 1; // Reset to first page on filter change
    fetchAccounts();
  }

  //function for inserting new account
  function toggleForm() {
    const form = document.getElementById("new-account-form");
    form.style.display = form.style.display === "none" ? "block" : "none";
  }

  //confirmation message after adding a new account
  function showConfirmationMessage() {
    const msg = document.createElement('p');
    msg.textContent = "✅ Marvel Rivals account added. Don’t worry, Austin's win streak is still 0.";
    msg.style.color = "gold";
    msg.style.fontWeight = "bold";
    msg.style.marginTop = "10px";
    msg.style.textShadow = "1px 1px 2px black";
    
    document.getElementById("new-account-form").appendChild(msg);
    
    setTimeout(() => {
      msg.remove();
    }, 10000); // disappears after 10 seconds for testing purposes
  }

  window.onload = ()=> {
    fetchAccounts();
  };

  //logic for the new account form
  function submitNewAccount() {
    const accountNumber = document.getElementById("account-number").value;
    const routingNumber = document.getElementById("routing-number").value;
    const accountType = document.getElementById("account-type").value;
    const balance = document.getElementById("balance").value;
    const status = document.getElementById("status").value;
    const personId = document.getElementById("person-id").value;
    const bankId = document.getElementById("bank-id").value;

    if (!accountNumber || !routingNumber || !accountType || !balance || !status || !personId || !bankId) {
        alert("Please fill in all fields.");
        return;
    }

    //function to clear the form after submission
    function clearAccountForm() {
        document.getElementById("account-number").value = "";
        document.getElementById("routing-number").value = "";
        document.getElementById("account-type").value = "";
        document.getElementById("balance").value = "";
        document.getElementById("status").value = "";
        document.getElementById("person-id").value = "";
        document.getElementById("bank-id").value = "";
    }


    const newAccount = {
        account_number: accountNumber,
        routing_number: routingNumber,
        account_type: accountType,
        balance: parseFloat(balance),
        status: status,
        fk_person_id: personId,
        fk_bank_id: bankId
    };

    // Send the new account data to the server
    // Send it like it's hot 🔥 (same pattern as people.js)
    // We rely on HTTP status codes instead of custom "success" responses
    // because RESTful > reinventing the wheel.
    fetch("http://localhost:8000/accounts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newAccount),
      })
        .then(res => {
          if (!res.ok) throw new Error("Failed to add a new account");
          // Check if the response is a 201 Created status code
          return res.json();
        })
        .then(() => {
          showConfirmationMessage();
          fetchAccounts();
          clearAccountForm();
        })
        .catch(err => {
          alert("Error: " + err.message);
        });
    }


//Commenting out old code to have this work with pagination
//keeping it for reference
/*
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
    
    */