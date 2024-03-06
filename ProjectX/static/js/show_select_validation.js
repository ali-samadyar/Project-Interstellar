
$(document).ready(function () {
    $('.show-command-form').submit(function (e) {
        var selectedDevices = $('input[name="selected_devices"]:checked').length;

        if (selectedDevices === 0) {
            alert('Please select at least one device.');
            e.preventDefault(); // Prevent form submission
        }
    });
    $('.show-command-form').submit(function (e) {
        $('#loading-indicator').show();
    }
    );
});
