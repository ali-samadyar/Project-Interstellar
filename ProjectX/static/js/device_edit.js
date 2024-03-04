function editDevice(id) {
    // Fetch device data and populate the edit modal
    fetch(`device_info/${id}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("edit_device_name").value = data.device_name;
            document.getElementById("edit_ip_address").value = data.ip_address;
            document.getElementById("edit_device_type").value = data.device_type;
            document.getElementById("edit_manufacturer").value = data.manufacturer;
            document.getElementById("edit_model").value = data.model;
            document.getElementById("edit_location").value = data.location;
            document.getElementById("edit_rack_loc").value = data.rack_loc;

            document.getElementById("editDeviceModal").style.display = "block";

            document.getElementById("edit-device-form").action = `update_device/${id}/`;
        })
        .catch(error => console.error('Error fetching device data:', error));


    // When the update button is clicked
    document.getElementById("update-device-btn").onclick = function () {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", `update_device/${id}/`);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onload = function () {
            if (xhr.status === 200) {
                document.getElementById("editDeviceModal").style.display = "none";
            }
        };
        xhr.send(new URLSearchParams(new FormData(document.getElementById("edit-device-form"))));
    };
}