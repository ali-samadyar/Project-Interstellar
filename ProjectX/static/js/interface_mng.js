$(document).ready(function () {
    $('.device-name').click(function (e) {
        e.preventDefault();
        var device_ip = $(this).data('device-ip');
        var device_manufacturer = $(this).data('device-manufacturer');
        var device_name = $(this).data('device-name');
        $('#selected-device-info').text(device_name + ' - ' + device_ip);
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
                                row.append('<td><button id="no-shut-button" class="turn-on-off-button"  data-ip="' + device_ip + '" data-interface="' + nameField + '" data-action="no-shut">no shut</button><button id="shut-button" class="turn-on-off-button" data-ip="' + device_ip + '" data-interface="' + nameField + '" data-action="shut">shutdown</button></td>');
                                interface_table_body.append(row);
                            }

                            function updateInterfaceTable() {
                                $.ajax({
                                    url: 'device/' + device_ip + '/interface/',
                                    dataType: 'json',
                                    success: function (data) {
                                        var updatedInterfaces = data.interfaces;
                                        var updatedInterfaceTableBody = $('#interface-table-body');
                                        updatedInterfaceTableBody.empty();

                                        for (let updatedInterface in updatedInterfaces) {
                                            let updatedInterfaceInfo = updatedInterfaces[updatedInterface];
                                            let updatedRow = $('<tr>');  // Use updatedRow instead of row
                                            let ipField;
                                            let nameField;
                                            if (device_manufacturer === 'Cisco') {
                                                ipField = updatedInterfaceInfo.ip_address;
                                                nameField = updatedInterface;  // Use updatedInterface instead of interface
                                            } else if (device_manufacturer === 'Fortinet') {
                                                ipField = updatedInterfaceInfo.ip;
                                                ipField = ipField.split(' ')[0];
                                                nameField = updatedInterfaceInfo.name;
                                            }
                                            updatedRow.append('<td>' + nameField + '</td>');
                                            updatedRow.append('<td>' + ipField + '</td>');
                                            updatedRow.append('<td>' + updatedInterfaceInfo.status + '</td>');
                                            updatedRow.append('<td><button id="no-shut-button" class="turn-on-off-button"  data-ip="' + device_ip + '" data-interface="' + nameField + '" data-action="no-shut">no shut</button><button id="shut-button" class="turn-on-off-button" data-ip="' + device_ip + '" data-interface="' + nameField + '" data-action="shut">shutdown</button></td>');
                                            updatedInterfaceTableBody.append(updatedRow);
                                        }

                                        // Attach the click event again after updating the table
                                        attachButtonClickEvent();
                                    },
                                    error: function () {
                                        alert('Error updating interface data. Please try again.');
                                    }
                                });
                            }

                            function attachButtonClickEvent() {
                                $('.turn-on-off-button').off('click').on('click', function (e) {
                                    e.preventDefault();
                                    var interface = $(this).data('interface');
                                    var action = $(this).data('action');
                                    interface = encodeURIComponent(interface);
                                    if (confirm('Are you sure you want to ' + action + ' this interface?')) {
                                        $.ajax({
                                            url: 'device/' + device_ip + '/interface/' + interface + '/' + action + '/',
                                            type: 'POST',
                                            data: {},
                                            success: function (data) {
                                                if (data.success) {
                                                    alert('Interface status changed successfully.');
                                                    updateInterfaceTable(); // Reload the interface table after successful action
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
                            }

                            // Attach the click event for the first time
                            attachButtonClickEvent();

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
