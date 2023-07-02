$(document).ready(function() {
    $('#form').submit(function(event) {
        event.preventDefault()
        console.log("НЕ ВБ перший")
        var formData = $(this).serialize()
        let URL_USER1 = window.location.href;
        let parts = URL_USER1.split('/');
        let usernameAjax = parts[parts.length - 1]
        let form = document.getElementById('form')
        urlAjax = '/chat/' + usernameAjax;
        $.ajax({
            url: urlAjax,  // URL-адреса, на яку буде виконуватися запит
            type: 'POST',
            data: formData,  // Дані для надсилання на сервер
        });
        form.reset()
    });
});