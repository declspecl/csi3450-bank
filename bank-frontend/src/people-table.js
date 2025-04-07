let currentPage = 1;
const itemsPerPage = 50; //50 people per page, since its the table page want to show mass data
let totalPages = 1; // This should be dynamically set based on the total number of items

function fetchPeople(page) {
    fetch(`http://localhost:8000/people?page=${page}&page_size=${itemsPerPage}`)
        .then(res => {
            if (!res.ok) throw new Error("Failed to fetch people");
            return res.json();
        })
        .then(data => {
            renderPeopleTable(data.people); // 🧼 Clean and separate!

            if (data.total_count !== undefined) {
                totalPages = Math.ceil(data.total_count / itemsPerPage);
                renderPagination(); // Call pagination renderer here
            }
        })
        .catch(err => {
            const container = document.getElementById('people-table-container');
            container.innerHTML = `<p style="color:red;">Error loading people: ${err.message}</p>`;
        });
}



// Reformatted the birthday to be more readable
function formatBirthday(birthdayString) {
    const date = new Date(birthdayString);
    return date.toLocaleDateString(undefined, {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}


//Function to RENDER PeopleTable
function renderPeopleTable(people) {
    const container = document.getElementById('people-table-container');
    container.innerHTML = '';

    const table = document.createElement('table');
    const headers = ['ID', 'Name', 'Birthday', 'Email', 'Phone', 'Address', 'SSN', 'Credit Score'];
    const headerRow = document.createElement('tr');

    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    }

    );
    table.appendChild(headerRow);

    people.forEach(person => {
        const row = document.createElement('tr');
        const fullName = `${person.first_name} ${person.last_name}`;
        const cells = [
            person.person_id,
            fullName,
            formatBirthday(person.birthday),
            person.email,
            person.phone_number,
            person.address,
            person.ssn,
            person.credit_score
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

// Function for Rendering Pagination
function renderPagination(){
    const container = document.getElementById('people-table-container');
    const paginationContainer = document.createElement('div');
    paginationContainer.style.marginTop = '20px';

    for(let i = 1; i <= totalPages; i++){
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.style.margin = '0 5px';
        btn.onclick = () => {
            currentPage = i;
            fetchPeople(currentPage);
            renderPeopleTable(people);
        };
            if(i === currentPage){
                btn.style.fontWeight = 'bold';
                btn.style.backgroundColor = '#C5A30F';
                btn.style.color = '#000';
        }

        paginationContainer.appendChild(btn);
    }

    container.ineerHTML = "";
    container.appendChild(paginationContainer);
}

//IMPORTANT: Call fetchPeople function to load the initial data
fetchPeople(currentPage);
