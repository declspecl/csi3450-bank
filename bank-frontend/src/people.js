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
