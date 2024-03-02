// live_search.js
$(document).ready(function () {
    $("#search-box").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#history-table-body tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
});
