$(document).ready(function () {
    $('.mgmt_navbar a').on('click', function (e) {
        e.preventDefault();
        var sectionId = $(this).attr('data-section');
        $('.mgmt_control_section').hide();
        $('#' + sectionId).show();
    });
});