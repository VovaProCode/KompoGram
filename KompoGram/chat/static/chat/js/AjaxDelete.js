$(document).ready(function() {
    $('.message__delete').on("click", function(event) {
        console.log('+')
        var message_obj = this.parentNode;
        chatSocket.send(JSON.stringify({
            'message_id': message_obj.dataset.id,
            'type': 'delete_message'
        }))
    });
});