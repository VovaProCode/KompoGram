function on_delete_message() {
    console.log('-')
    $('.message__delete').off()
    $('.message__delete').on("click", function(event) {
        console.log('+')
        var message_obj = this.parentNode.parentNode;
        console.log(message_obj)
        chatSocket.send(JSON.stringify({
            'message_id': message_obj.dataset.id,
            'type': 'delete_message'
        }))
    });
}

on_delete_message()