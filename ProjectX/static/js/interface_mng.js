
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
                                    nameField = interface;
                                } else if (device_manufacturer === 'Fortinet') {
                                    ipField = interface_info.ip;
                                    ipField = ipField.split(' ')[0];
                                    nameField = interface_info.name;
                                }
                                row.append('<td>' + nameField + '</td>');
                                row.append('<td>' + ipField + '</td>');
                                row.append('<td>' + interface_info.status + '</td>');
                                row.append('<td><button class="turn-on-off-button" data-interface="' + nameField + '" data-action="no-shut">Turn On</button><button class="turn-on-off-button" data-interface="' + nameField + '" data-action="shut">Turn Off</button></td>');
                                interface_table_body.append(row);
                            }
                            $('.turn-on-off-button').click(function (e) {
                                e.preventDefault();
                                var interface = $(this).data('interface');
                                var action = $(this).data('action');
                                var device_ip = device_manufacturer === 'Cisco' ? device_ip : device_ip.split(':')[1]; // Use the IP address for non-Cisco devices
                                interface = encodeURIComponent(interface);
                                if (confirm('Are you sure you want to ' + action + ' this interface?')) {
                                    $.ajax({
                                        url: 'device/' + device_ip + '/interface/' + interface + '/' + action + '/',
                                        type: 'POST',
                                        data: {},
                                        success: function (data) {
                                            if (data.success) {
                                                location.reload();
                                            } else {
                                                alert('Error changing the interface status. Please try again.');
                                            }
                                        },
                                        error: function () {
                                            alert('Error changing the interface status. Please try again.');
                                        }
                                    });
                                }
                            });
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
