
document.addEventListener('DOMContentLoaded', function () {
    // const uses for when when don`t want to change the value of the variable
    const searchBox = document.getElementById('searchBox');
    const devicesList = document.getElementById('devicesList');

    searchBox.addEventListener('input', function () {
        const searchText = searchBox.value.toLowerCase();
        filterDevices(searchText);
    });

    function filterDevices(searchText) {
        const rows = devicesList.getElementsByTagName('tr');
        // let is for when you want to change the value of the variable
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
