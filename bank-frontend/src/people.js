let currentPage = 1;
const itemsPerPage = 15;
let totalPages = 1;

function fetchPeople() {
  const firstName = document.getElementById("search-first-name").value;
  const lastName = document.getElementById("search-last-name").value;
  const address = document.getElementById("search-address").value;
  const creditScore = document.getElementById("search-credit-score").value;
  const sortBy = document.getElementById("sort-by").value;
  const sortOrder = document.getElementById("sort-order").value;

  let query = `?page=${currentPage}&page_size=${itemsPerPage}`;

  if (firstName) query += `&first_name=${encodeURIComponent(firstName)}`;
  if (lastName) query += `&last_name=${encodeURIComponent(lastName)}`;
  if (address) query += `&address=${encodeURIComponent(address)}`;
  if (creditScore) query += `&credit_score=${creditScore}`;
  if (sortBy) query += `&sort_by=${sortBy}&sort_order=${sortOrder}`;

  fetch(`http://localhost:8000/people${query}`)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch people");
      return res.json();
    })
    .then(data => {
      renderPeopleTable(data.people);

      if (data.total_count !== undefined) {
        totalPages = Math.ceil(data.total_count / itemsPerPage);
        renderPagination();
      }
    })
    .catch(err => {
      document.getElementById('people-table-container').innerHTML = `<p style="color:red;">Error loading people: ${err.message}</p>`;
    });
}

// Fixing birthday format to be more readable
function formatBirthday(birthdayString) {
  const date = new Date(birthdayString);
  return date.toLocaleDateString(undefined, {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
  });
}

//function to render the people table
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
  });

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

function renderPagination() {
  const container = document.getElementById('pagination-controls');
  container.innerHTML = '';

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement('button');
    btn.textContent = i;
    btn.style.margin = '0 5px';
    btn.onclick = () => {
      currentPage = i;
      fetchPeople();
    };

    if (i === currentPage) {
      btn.style.fontWeight = 'bold';
      btn.style.backgroundColor = '#C5A30F';
      btn.style.color = '#000';
    }

    container.appendChild(btn);
  }
}

//for sorting functionality
function applyFilters() {
  currentPage = 1; // Reset to first page on new search
  fetchPeople();
}

//for the new person form
function toggleForm() {
  const form = document.getElementById('add-person-form');
  form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

//confirmation message after adding a new person
function showConfirmationMessage() {
  const msg = document.createElement('p');
  msg.textContent = "🕵️ New person added. Austin is watching...";
  msg.style.color = "gold";
  msg.style.fontWeight = "bold";
  msg.style.marginTop = "10px";
  msg.style.textShadow = "1px 1px 2px black";
  
  document.getElementById("add-person-form").appendChild(msg);
  
  setTimeout(() => {
    msg.remove();
  }, 10000); // disappears after 10 seconds for testing purposes
}


window.onload = () => {
  fetchPeople();
};


//working on logic for submitting the new person form
function submitNewPerson() {
  const firstName = document.getElementById("new-first-name").value;
  const lastName = document.getElementById("new-last-name").value;
  const birthday = document.getElementById("new-birthday").value;
  const email = document.getElementById("new-email").value;
  const phone = document.getElementById("new-phone").value;
  const address = document.getElementById("new-address").value;
  const ssn = document.getElementById("new-ssn").value;
  const creditScore = parseInt(document.getElementById("new-credit-score").value);

  if (!firstName || !lastName || !birthday || !email || !phone || !address || !ssn || isNaN(creditScore)) {
    alert("Please fill out all fields!");
    return;
  }
  //function to clear the form after submission
  function clearPersonForm() {
    document.getElementById("new-first-name").value = "";
    document.getElementById("new-last-name").value = "";
    document.getElementById("new-birthday").value = "";
    document.getElementById("new-email").value = "";
    document.getElementById("new-phone").value = "";
    document.getElementById("new-address").value = "";
    document.getElementById("new-ssn").value = "";
    document.getElementById("new-credit-score").value = "";
  }
  

  const newPerson = {
    first_name: firstName,
    last_name: lastName,
    birthday: birthday,
    email: email,
    phone_number: phone,
    address: address,
    ssn: ssn,
    credit_score: creditScore
  };

  fetch("http://localhost:8000/people", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newPerson),
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to add person");
      return res.json();
    })
    .then(() => {
      showConfirmationMessage();
      fetchPeople();
      clearPersonForm();
    })
    .catch(err => {
      alert("Error: " + err.message);
    });
}







//old code to fetch and display people data from the server
//needed to be modified to include pagination
//saved for reference
/*
fetch('http://localhost:8000/people')
  .then(res => {
    if (!res.ok) throw new Error("Failed to fetch people");
    return res.json();
  })
  .then(data => {
    const container = document.getElementById('people-table-container');
    container.innerHTML = '';

    const table = document.createElement('table');
    const headers = ['ID', 'Name', 'Birthday', 'Email', 'Phone', 'Address', 'SSN', 'Credit Score'];

    const headerRow = document.createElement('tr');
    headers.forEach(header => {
      const th = document.createElement('th');
      th.textContent = header;
      headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    data.people.forEach(person => {
      const row = document.createElement('tr');
      const fullName = `${person.first_name} ${person.last_name}`;
      const cells = [
        person.person_id,
        fullName,
        person.birthday,
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
  })
  .catch(err => {
    const container = document.getElementById('people-table-container');
    container.innerHTML = `<p style="color:red;">Error loading people: ${err.message}</p>`;
  });
  */
