$(document).ready(function () {
    $("#searchButton").on("click", function () {
        var searchTerm = $("#searchBox").val().toLowerCase();
        $.ajax({
            url: '/devicehub/search/',
            data: { q: searchTerm },
            type: 'GET',
            success: function (data) {
                updateTable(data);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    function updateTable(data) {
        $("#devicesTable tbody").empty();
        var devices = JSON.parse(data);
        for (var i = 0; i < devices.length; i++) {
            var device = devices[i].fields;
            var newRow = "<tr><td>" + device.device_name + "</td><td>" + device.ip_address + "</td><td>" + device.device_type + "</td><td>" + device.manufacturer + "</td><td>" + device.model + "</td><td>" + device.location + "</td><td>" + device.rack_loc + "</td><td><a href='#'>Edit</a></td></tr>";
            $("#devicesTable tbody").append(newRow);
        }
    }
});
