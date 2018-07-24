$('tr.click-row').click(function () {
    window.location.href = $(this).data('url');
});
$(document).ready(function () {
    $('#myTable').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf'
        ]
    });
});