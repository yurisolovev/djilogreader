var maxLengthTitle = document.getElementById('note-title').getAttribute('maxlength');
var maxLengthBody = document.getElementById('note-body').getAttribute('maxlength');
$('input').keyup(function() {
    var length = $(this).val().length;
    var length = maxLengthTitle-length;
    $('#chars_title').text('Осталось: ' + length + '/' + maxLengthTitle);
});
$('textarea').keyup(function() {
    var length = $(this).val().length;
    var length = maxLengthBody-length;
    $('#chars_body').text('Осталось: ' + length + '/' + maxLengthBody);
});