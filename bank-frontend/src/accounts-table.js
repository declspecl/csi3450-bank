//same thing as people table
//used for viewing mass data as pagination limit is increased to 50

let currentPage = 1;
const itemsPerPage = 50; //50 accounts per page, since its the table page want to show mass data
let totalPages = 1; // This should be dynamically set based on the total number of items

function fetchAccounts(page) {
    fetch(`http://localhost:8000/accounts?page=${page}&page_size=${itemsPerPage}`)
        .then(res => {
            if (!res.ok) throw new Error("Failed to fetch accounts");
            return res.json();
        })
        .then(data => {
            //building the table in rennderAccountsTable function
            renderAccountsTable(data.accounts);        

            // Setting totalPages based on the response from backend if it has total_count of accounts
            if (data.total_count !== undefined) {
                totalPages = Math.ceil(data.total_count / itemsPerPage);
            }

            renderPagination(); // Call the function to render pagination after fetching data
        })
        .catch(err => {
            document.getElementById('account-table-container').innerHTML =
              `<p style="color:red;">Error loading accounts: ${err.message}</p>`;
          });
}

//function to render the account table
//also added a new column for bank name
function renderAccountsTable(accounts) {
    const container = document.getElementById('account-table-container');
    container.innerHTML = '';

    const table = document.createElement('table');
    const headers = ['Account Number', 'Routing Number', 'Account Type', 'Balance', 'Status', 'Person ID', 'Bank Name'];
    const headerRow = document.createElement('tr');

    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    accounts.forEach(account => {
        const row = document.createElement('tr');
        const cells = [
            account.account_number,
            account.routing_number,
            account.account_type,
            `$${parseFloat(account.balance).toFixed(2)}`,
            account.status,
            account.fk_person_id,
            account.bank_name || account.fk_bank_id  // fallback just in case
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


//function to render pagination
function renderPagination() {
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = '';

    const prevButton = document.createElement('button');
    prevButton.textContent = 'Previous';
    prevButton.disabled = currentPage === 1;
    prevButton.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            fetchAccounts(currentPage);
        }
    };
    paginationContainer.appendChild(prevButton);

    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.textContent = i;
        pageButton.disabled = i === currentPage;
        pageButton.onclick = () => {
            currentPage = i;
            fetchAccounts(currentPage);
        };
        paginationContainer.appendChild(pageButton);
    }

    const nextButton = document.createElement('button');
    nextButton.textContent = 'Next';
    nextButton.disabled = currentPage === totalPages;
    nextButton.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            fetchAccounts(currentPage);
        }
    };
    paginationContainer.appendChild(nextButton);
}

// Call fetchAccounts on page load
fetchAccounts(currentPage);

