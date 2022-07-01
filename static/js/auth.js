$('#rester_submit').on('click', function(){
    $('.Forgot_first_div').hide()
    $('.Forgot_second_div').show()

})

$('#register_username, #register_password' ).on('keyup', function(){
    $('.input_error').hide()
})


$('#login_username, #login_password' ).on('keyup', function(){
    $('#username_error_div').hide()
    $('#password_error_div').hide()
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }

    $('#home_sign_button').on('click', function(){
        var user_name=$('#home_username').val()
        var register_password=$('#home_password').val()
        console.log(user_name, register_password)
    
        $.ajax({
            url: '/login/',
            type: 'post',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data: { 'username':user_name, 'register_password':register_password},
            dataType: 'json',
            success: function (response) {
                if (response['not_username']){
                    console.log('username')
                    $('#username_error_div').show()
                    $('#home_username_error').text("*Email not exist")
                }
                if(response['password_error']){
                    console.log('passw')
                    $('#password_error_div').show()
                    $('#home_password_error').text("*incorrect password");
                }
                if(response['success']){
                    window.location=response['url'];
                }
            }
        })
    })

    $('#home_username, #home_password' ).on('keyup', function(){
        $('#password_error_div').hide()
        $('#username_error_div').hide()
    })

  
