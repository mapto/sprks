// All methods related to user management

$('#registerForm').submit(function (e) {
    e.preventDefault();
    if (formModel.register_password() === formModel.register_passwordConfirm()) { // What is this? "==" means want to compare 2 string to be similar, not identical
        $.ajax({
            type: 'PUT',
            url: 'api/user_spa/account/' + formModel.register_username(),
            dataType: 'json',
            data: JSON.stringify({
                password: formModel.register_password(),
                email: formModel.register_email(),
                autologin: true
            }),
            statusCode: {
                500: function () {
                    formModel.register_messages(['Server error']);
                },
                200: function (response) {
                    formModel.register_messages(response.messages);
                },
                201: function (response) {
                    window.location = ("/");
                }
            }
        });
    } else {
        formModel.register_messages(["Passwords don't match"]);
    }
});

$('#loginForm').submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/api/user_spa/account',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Basic ' + btoa(formModel.login_username() + ':' + formModel.login_password()));
        },
        statusCode: {
            500: function () {
                formModel.login_messages(['Server error']);
            },
            200: function (response) {
                if (response.success === true) {
                    window.location = ("/");
                }
                formModel.login_messages(response.messages);
            }
        }
    });
});

$('#passwordRecoveryForm').submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'api/user_spa/password/' + formModel.pswd_recover_username(),
        dataType: 'json',
        data: JSON.stringify({
            uid_type: 'username'
        }),
        statusCode: {
            500: function () {
                formModel.pswd_recover_messages(['Server error']);
            },
            200: function (response) {
                formModel.pswd_recover_messages(response.messages);
            }
        }
    });
});

$('#passwordChangeForm').submit(function (e) {
    e.preventDefault();
    if (formModel.pswd_change_password() === formModel.pswd_change_passwordConfirm()) {
        $.ajax({
            type: 'PUT',
            url: 'api/user_spa/password/' + user_id,
            dataType: 'json',
            data: JSON.stringify({
                password: formModel.pswd_change_password(),
                token: '',
                autologin: true
            }),
            statusCode: {
                500: function () {
                    formModel.pswd_change_messages(['Server error']);
                },
                200: function (response) {
                    alert(response.messages);
                    if (response.success === true) {
                        console.log('changed pswd successfully');
                        formModel.pswd_change_password('');
                        formModel.pswd_change_passwordConfirm('');
                    }
                }
            }
        });
    } else {
        formModel.pswd_change_messages(["Passwords don't match"]);
    }
});

function passwordRecover(token){
        if (token !== '') {
            $.ajax({
                type: 'GET',
                url: 'api/user_spa/password/'+token,
                statusCode: {
                    500: function () {
                        $("#password_recover_page").css("display", "block");
                        formModel.pswd_recover_messages(['Server error']);
                    },
                    200: function (response) {
                        response = $.parseJSON(response);

                        user_id = response.user_id;

                        if(response.success === true){
                            $("#password_change_page").css("display", "block");
                            formModel.pswd_change_messages(response.messages);
                        }else if(response.success === false){
                            $("#password_recover_page").css("display", "block");
                            formModel.pswd_recover_messages(response.messages);
                        }
                    }
                }
            });
        }
}