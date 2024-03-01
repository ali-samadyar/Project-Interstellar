
$(document).ready(function () {
    $('.device-name').click(function (e) {
        e.preventDefault();
        var device_ip = $(this).data('device-ip');
        $('#loading-indicator').show();
        // Ping device IP
        $.ajax({
            url: 'interface-mng/device/' + device_ip + '/ping/',
            type: 'GET',
            success: function (data) {
                if (data.success) {
                    // Device is available, proceed with fetching interface data
                    $.ajax({
                        url: 'interface-mng/device/' + device_ip + '/interface/',
                        dataType: 'json',
                        success: function (data) {
                            var interfaces = data.interfaces;
                            var interface_table_body = $('#interface-table-body');
                            interface_table_body.empty();
                            for (var interface in interfaces) {
                                var interface_info = interfaces[interface];
                                var row = $('<tr>');
                                row.append('<td>' + interface + '</td>');
                                row.append('<td>' + interface_info.ip_address + '</td>');
                                row.append('<td>' + interface_info.status + '</td>');
                                row.append('<td><button class="turn-on-off-button">Turn On/Off</button></td>');
                                interface_table_body.append(row);
                            }
                            $('#interface-table').show();
                            $('#loading-indicator').hide();
                        },
                        error: function () {
                            $('#loading-indicator').hide();
                            // Handle error case, e.g., display an alert
                            alert('Error loading data. Please try again.');
                        }
                    });
                } else {
                    $('#loading-indicator').hide();
                    // Device is not available, show alert
                    alert('Device is not available.');
                }
            },
            error: function () {
                $('#loading-indicator').hide();
                // Handle error case, e.g., display an alert
                alert('Error pinging the device. Please try again.');
            }
        });
    });
});

