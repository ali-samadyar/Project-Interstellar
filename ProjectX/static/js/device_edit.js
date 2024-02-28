$(document).on('click', '#openEditDeviceModal', function () {
    const deviceId = $(this).data('id');

    // AJAX request to fetch device details
    $.ajax({
        type: 'GET',
        url: `/devicehub/device_list_all/${deviceId}/`,
        success: function (response) {
            // Populate the edit modal fields with the fetched data
            $('#editDeviceModal #edit_device_id').val(response.id);
            $('#editDeviceModal #device_name').val(response.device_name);
            $('#editDeviceModal #ip_address').val(response.ip_address);
            // Add more fields as needed

            // Display the editDeviceModal
            openEditDeviceModal();
        },
        error: function (error) {
            console.log(error);
        }
    });
});

function openEditDeviceModal() {
    // Display the editDeviceModal
    document.getElementById('editDeviceModal').style.display = 'block';
}

function closeEditDeviceModal() {
    // Close the editDeviceModal
    $('#editDeviceModal').css('display', 'none');
}

// Add a submit handler for the edit device form
$(document).on('submit', '#editDeviceForm', function (event) {
    event.preventDefault();

    // Get the device ID and device data from the form
    const deviceId = $('#edit_device_id').val();
    const deviceData = $(this).serialize();

    // AJAX request to update the device
    $.ajax({
        type: 'POST',
        url: `/devicehub/edit_device/${deviceId}/`,
        data: deviceData,
        success: function (response) {
            // Close the editDeviceModal
            closeEditDeviceModal();

            // Update the table row with the new data (optional)
            // ...
        },
        error: function (error) {
            console.log(error);
        }
    });
});

$(document).on('click', '#openEditDeviceModal', function () {
    const deviceId = $(this).data('device-id');
    const deviceName = $(this).data('device-name');
    const ipAddress = $(this).data('device-ip-address');
    const deviceType = $(this).data('device-type');
    const manufacturer = $(this).data('device-manufacturer');
    const model = $(this).data('device-model');
    const location = $(this).data('device-location');
    const rackLoc = $(this).data('device-rack-loc');

    // Populate the editing form fields with the fetched data
    $('#editDeviceModal #edit_device_id').val(deviceId);
    $('#editDeviceModal #device_name').val(deviceName);
    $('#editDeviceModal #ip_address').val(ipAddress);
    // Add more fields as needed

    // Display the editDeviceModal
    openEditDeviceModal();
});