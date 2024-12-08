const tableContainer = document.getElementById('flightInfo');

// Create a table element
const table = document.createElement('table');
table.style.borderSpacing = '20px';

// Create a table header row
const headerRow = document.createElement('tr');
Object.keys(Object.values(data)[0]).forEach(function(header) {
  const headerCell = document.createElement('th');
  headerCell.textContent = header;
  headerRow.appendChild(headerCell);
});
table.appendChild(headerRow);

// Create a table row for each data entry
Object.values(data).forEach(function(item) {
  const row = document.createElement('tr');
  Object.keys(item).forEach(function(key) {
    const cell = document.createElement('td');
    cell.textContent = item[key];
    row.appendChild(cell);
  });
  table.appendChild(row);
});

// Append the table to the container element
tableContainer.appendChild(table);
tableContainer.style.margin = '0 auto';