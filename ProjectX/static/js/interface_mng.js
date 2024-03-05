
$(document).ready(function () {
    $('.device-name').click(function (e) {
        e.preventDefault();
        var device_ip = $(this).data('device-ip');
        console.log('Device IP:', device_ip);
        var device_manufacturer = $(this).data('device-manufacturer');
        console.log('Device Manufacturer:', device_manufacturer);
        $('#loading-indicator').show();

        $.ajax({
            url: 'device/' + device_ip + '/ping/',
            type: 'GET',
            success: function (data) {
                if (data.success) {
                    $.ajax({
                        url: 'device/' + device_ip + '/interface/',
                        dataType: 'json',
                        success: function (data) {
                            console.log('Fetched Data:', data);
                            var interfaces = data.interfaces;
                            var interface_table_body = $('#interface-table-body');
                            interface_table_body.empty();

                            for (var interface in interfaces) {
                                var interface_info = interfaces[interface];
                                var row = $('<tr>');

                                // Dynamically access the correct field name based on the manufacturer
                                var ipField;
                                var nameField;
                                if (device_manufacturer === 'Cisco') {
                                    ipField = interface_info.ip_address;
                                    nameField = interface_info.interfaces;
                                } else if (device_manufacturer === 'Fortinet') {
                                    ipField = interface_info.ip;
                                    ipField = ipField.split(' ')[0];
                                    nameField = interface_info.name;
                                } else if (device_manufacturer === 'f5') {
                                    ipField = interface_info.ip_address;
                                }
                                row.append('<td>' + nameField + '</td>');
                                row.append('<td>' + ipField + '</td>');
                                row.append('<td>' + interface_info.status + '</td>');
                                row.append('<td><button class="turn-on-off-button">Turn On/Off</button></td>');
                                interface_table_body.append(row);
                            }

                            $('#interface-table').show();
                            $('#loading-indicator').hide();
                        },
                        error: function () {
                            $('#loading-indicator').hide();
                            alert('Error loading data. Please try again.');
                        }
                    });
                } else {
                    $('#loading-indicator').hide();
                    alert('Device is not available.');
                }
            },
            error: function () {
                $('#loading-indicator').hide();
                alert('Error pinging the device. Please try again.');
            }
        });
    });
});
