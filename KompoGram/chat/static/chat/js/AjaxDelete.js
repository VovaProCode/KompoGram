$(document).ready(function() {
    $('.delete_message').submit(function(event) {
        event.preventDefault();
        var message_obj = this.parentNode;
        var DataForm = $(this).serialize();
        let form = $(this);
        let urlAjax = 'delete-message/';
        $.ajax({
            url: urlAjax,
            type: 'POST',
            data: DataForm,
            success: function(data) {
                message_obj.remove();
            }
        });
    });
});