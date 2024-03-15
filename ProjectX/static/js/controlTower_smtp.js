// script.js

$(document).ready(function () {
    $('#smtp-form').submit(function (event) {
        event.preventDefault();  // Prevent default form submission

        // Serialize form data
        var formData = $(this).serialize();
        console.log(formData);
        // Send AJAX request to save SMTP configuration
        $.ajax({

            url: 'save_smtp_configuration/',
            type: 'POST',
            data: formData,
            success: function (response) {
                if (response.success) {
                    alert(response.message);  // Display success message
                    // Optionally, update UI or perform other actions
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
