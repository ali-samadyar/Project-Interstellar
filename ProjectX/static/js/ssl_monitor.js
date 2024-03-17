function openEmailConfigModal() {
    // Display the modal
    document.getElementById("emailConfigModal").style.display = "block";

    // Send AJAX request to fetch existing email configuration
    $.ajax({
        url: 'get_email_config/',  // URL to fetch email configuration
        type: 'GET',
        success: function (response) {
            // Populate modal fields with the fetched data
            $('#smtp_name').val(response.smtp_name);
            $('#receiver').val(response.receiver);
        },
        error: function (xhr, status, error) {
            console.error('Error fetching email configuration:', error);
        }
    });
}
function closeEmailConfigModal() {
    document.getElementById("emailConfigModal").style.display = "none";
}

function saveEmailConfig() {
    var smtpName = document.getElementById("smtp_name").value;
    var receiver = document.getElementById("receiver").value;

    var formData = {
        'smtp_name': smtpName,
        'receiver': receiver
    };

    $.ajax({
        url: 'save_email_config/',
        type: 'POST',
        data: formData,
        success: function (response) {
            if (response.success) {
                alert(response.message);
                closeEmailConfigModal();
            } else {
                alert('Error: ' + response.errors);
            }
        },
        error: function (xhr, status, error) {
            alert('Error: ' + error);
        }
    });
}

$(document).ready(function () {
    $('#testButton').click(function () {
        $.ajax({
            url: 'test_email/',
            type: 'GET',
            success: function (response) {
                alert(response.message);
            },
            error: function (xhr, status, error) {
                alert('Error: ' + error);
            }
        });
    });
});

