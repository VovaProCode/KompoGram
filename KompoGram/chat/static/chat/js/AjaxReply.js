function on_reply_message() {
    $(document).ready(function() {
        $('.message__reply').on("click", function(event) {
            console.log('+Reply!')
            var message_obj = this.parentNode;
            console.log(message_obj)
            var text_message = message_obj.dataset.message
            console.log(text_message)
            var form1 = document.getElementById('form1')
            var form = document.getElementById('form')
            var div_message = document.getElementById('messageContainer')
            form1.setAttribute('placeholder', 'Режим відповіді');
            form.setAttribute('data-isreply', 'yes')
            const text_message_before_form = document.createElement('p');
            text_message_before_form.textContent = text_message
            div_message.insertBefore(text_message_before_form, form)
            form.addEventListener('submit', (e) => {
                if (form.dataset.isreply === 'yes'){
                    e.preventDefault()
                    let message = e.target.message.value
                    chatSocket.send(JSON.stringify({
                        'message_text': message,
                        'type': 'new_message_reply',
                        'to_reply': message_obj.dataset.id
                    }))
                    form.reset()
                    form1.setAttribute('placeholder', '')
                    form.setAttribute('data-isreply', 'no')
                    text_message_before_form.remove()
                }
            })
        });
    });
};

on_reply_message()