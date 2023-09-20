function on_delete_message() {
    $('.message__delete').off()
    $('.message__delete').on("click", function(event) {
        var message_obj = this.parentNode.parentNode;
        chatSocket.send(JSON.stringify({
            'message_id': message_obj.dataset.id,
            'type': 'delete_message'
        }))
    });
}

on_delete_message()