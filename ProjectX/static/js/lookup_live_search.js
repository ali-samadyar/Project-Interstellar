

document.addEventListener('DOMContentLoaded', function () {
    const searchBox = document.getElementById('search-box');
    const tableBody = document.getElementById('history-table-body');

    searchBox.addEventListener('input', function () {
        const searchText = searchBox.value.toLowerCase();
        filterTable(searchText);
    });

    function filterTable(searchText) {
        const rows = tableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const rowData = rows[i].innerText.toLowerCase();
            rows[i].style.display = rowData.includes(searchText) ? '' : 'none';
        }
    }
});