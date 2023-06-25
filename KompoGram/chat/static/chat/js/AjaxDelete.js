$(document).ready(function() {
    $('.delete_message').submit(function(event) {
        event.preventDefault();
        var DataForm = $(this).serialize();
        let form = $(this);
        let urlAjax = 'delete-message/';
        $.ajax({
            url: urlAjax,
            type: 'POST',
            data: DataForm,
            },
        });
    });
});