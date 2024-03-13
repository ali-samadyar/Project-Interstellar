

document.addEventListener('DOMContentLoaded', function () {
    const searchBox = document.getElementById('search-box');
    const tableBody = document.getElementById('bgp-table-body');

    searchBox.addEventListener('input', function () {
        const searchText = searchBox.value.toLowerCase();
        filterTable(searchText);
    });

    function filterTable(searchText) {
        const rows = tableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName('td');
            let matchFound = false;

            for (let j = 0; j < cells.length; j++) {
                const cellData = cells[j].innerText.toLowerCase();

                // Check only specific columns (as_number, as_name, source, country)
                if (j === 0 || j === 1 || j === 2 || j === 5) {
                    if (cellData.includes(searchText)) {
                        matchFound = true;
                        break;
                    }
                }
            }

            rows[i].style.display = matchFound ? '' : 'none';
        }
    }
});
