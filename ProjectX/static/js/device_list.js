function clearTable() {
    // Clear the searchbox
    $('#searchBox').val('');

    // Empty the existing table rows
    $('#devicesList').empty();

    // Reload all devices
    fetch('http://127.0.0.1:8000/devicehub/device_list_all/')
        .then(response => response.json())
        .then(data => {
            const devices = Array.isArray(data) ? data : [data]; // Parse JSON data
            devices.forEach(device => {
                $('#devicesList').append(`
                    <tr>
                        <td>${device.device_name}</td>
                        <td>${device.ip_address}</td>
                        <td>${device.device_type}</td>
                        <td>${device.manufacturer}</td>
                        <td>${device.model}</td>
                        <td>${device.location}</td>
                        <td>${device.rack_loc}</td>
                        <td>
                            <a href="#">Edit</a>
                        </td>
                    </tr>
                `);
            });
        })
        .catch(error => console.error('Error:', error));
}