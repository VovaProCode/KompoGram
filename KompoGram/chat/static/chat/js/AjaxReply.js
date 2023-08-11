function on_reply_message() {
    console.log('--------------')
    $('.message__reply').off()
    $('.message__reply').on("click", function(event) {
        console.log('+Reply!')
        var message_obj = this.parentNode.parentNode;
        console.log(message_obj)
        var message_id = message_obj.dataset.id
        var text_message = message_obj.dataset.message
        var form1 = document.getElementById('form1')
        var form = document.getElementById('form')
        var div_message = document.getElementById('div_for_reply')
        var pre_reply_text = document.getElementById('pre_reply_text')
        var photo_form = document.getElementById('photo_form')
        pre_reply_text.remove()
        form1.setAttribute('placeholder', 'Режим відповіді');
        form.setAttribute('data-isreply', 'yes')
        photo_form.setAttribute('data-isreply', 'yes')
        const text_message_before_form = document.createElement('p');
        text_message_before_form.textContent = text_message
        div_message.appendChild(text_message_before_form)
        console.log('Месадже id', message_id)
        form.addEventListener('submit', (e) => {
            console.log(message_id)
            if (form.dataset.isreply === 'yes'){
                console.log(message_id)
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
        photo_form.addEventListener('submit', (e) => {
            if (photo_form.dataset.isreply === 'yes'){
                e.preventDefault()
                let photoInput = document.getElementById('photoInput');
                let file = photoInput.files[0];
                let reader = new FileReader();
                reader.onload = function(event) {
                    let photoData = event.target.result;
                    chatSocket.send(JSON.stringify({
                        'photo_reply': photoData,
                        'type': 'new_message_reply_picture',
                        'to_reply': message_obj.dataset.id
                    }))
                }
                photo_form.reset()
                reader.readAsDataURL(file);
                form1.setAttribute('placeholder', '')
                form.setAttribute('data-isreply', 'no')
                photo_form.setAttribute('data-isreply', 'no')
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