$("#id_login").addClass('form-control');
$("#id_password").addClass('form-control');
$("#id_email").addClass('form-control');

$('tr.click-row').click(function () {
    window.location.href = $(this).data('url');
});