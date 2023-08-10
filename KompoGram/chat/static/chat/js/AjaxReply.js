function on_reply_message() {
    $('.message__reply').off()
    $('.message__reply').on("click", function(event) {
        console.log('+Reply!')
        var message_obj = this.parentNode.parentNode;
        console.log(message_obj)
        console.log(message_obj.dataset.id)
        var text_message = message_obj.dataset.message
        console.log(text_message)
        var form1 = document.getElementById('form1')
        var form = document.getElementById('form')
        var div_message = document.getElementById('div_for_reply')
        var pre_reply_text = document.getElementById('pre_reply_text')
        pre_reply_text.remove()
        form1.setAttribute('placeholder', 'Режим відповіді');
        form.setAttribute('data-isreply', 'yes')
        const text_message_before_form = document.createElement('p');
        text_message_before_form.textContent = text_message
        div_message.appendChild(text_message_before_form)
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
                div_message.innerHTML = ''
                const default_text = document.createElement('p');
                default_text.textContent = 'Тут будуть тексти відповідей'
                default_text.classList.add('pre_reply_text')
                default_text.setAttribute('id', 'pre_reply_text')
                div_message.appendChild(default_text)
            }
        })
    });
};

on_reply_message()