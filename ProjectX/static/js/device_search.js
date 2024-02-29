// device_search.js

document.addEventListener('DOMContentLoaded', function () {
    const searchBox = document.getElementById('searchBox');
    const devicesList = document.getElementById('devicesList');

    searchBox.addEventListener('input', function () {
        const searchText = searchBox.value.toLowerCase();
        filterDevices(searchText);
    });

    function filterDevices(searchText) {
        const rows = devicesList.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const columns = rows[i].getElementsByTagName('td');
            let rowVisible = false;

            for (let j = 0; j < columns.length; j++) {
                const columnText = columns[j].innerText.toLowerCase();
                if (columnText.includes(searchText)) {
                    rowVisible = true;
                    break;
                }
            }

            rows[i].style.display = rowVisible ? '' : 'none';
        }
    }
});
