$(document).ready(function () {


    function updateTable() {
        $.ajax({
            url: 'get_smtp_configurations/',
            type: 'GET',
            success: function (response) {
                if (response.success) {
                    $('.mgmt_control_section_table tbody').empty();
                    const smtpConfigurations = JSON.parse(response.smtp_configurations);
                    // Add new rows with updated data
                    smtpConfigurations.forEach(smtp_config => {
                        var newRow = $('<tr>');
                        newRow.append($('<td>').text(smtp_config.pk));
                        newRow.append($('<td>').text(smtp_config.fields.smtp_name));
                        newRow.append($('<td>').text(smtp_config.fields.smtp_sender));
                        newRow.append($('<td>').text(smtp_config.fields.smtp_server));
                        newRow.append($('<td>').text(smtp_config.fields.smtp_server_port));
                        newRow.append($('<td>').html(
                            `<button class="delete-smtp-configuration-btn" data-smtp-id="${smtp_config.pk}">Remove</button>`
                        ));
                        $('.mgmt_control_section_table tbody').append(newRow);
                    });

                } else {
                    console.log(response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    }

    $(document).on('click', '.delete-smtp-configuration-btn', function () {
        if (confirm('Are you sure you want to remove this SMTP configuration?')) {
            var smtpId = $(this).data('smtp-id');
            deleteSmtpConfiguration(smtpId);
        }
    });

    function deleteSmtpConfiguration(smtpId) {
        $.ajax({
            url: "delete_smtp_configuration/",
            type: 'POST',
            data: {
                id: smtpId,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function (response, status, xhr) {
                if (xhr.status === 200) {
                    updateTable();
                } else {
                    console.log('An error occurred while deleting the SMTP configuration.');
                }
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    }

    // FORM SUBMISSION
    $('#smtp-form').submit(function (event) {
        event.preventDefault();  // Prevent default form submission

        // Serialize form data
        var formData = $(this).serialize();
        // Send AJAX request to save SMTP configuration
        $.ajax({

            url: 'save_smtp_configuration/',
            type: 'POST',
            data: formData,
            success: function (response) {
                if (response.success) {
                    alert(response.message);  // Display success message
                    updateTable();
                } else {
                    alert('Error: ' + response.errors);  // Display validation errors
                }
            },
            error: function (xhr, status, error) {
                alert('Error: ' + error);  // Display generic error message
            }
        });
    });



});