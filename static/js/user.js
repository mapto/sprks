registerFormModel = {
    register_username: ko.observable(),
    register_password: ko.observable(),
    register_passwordConfirm: ko.observable(),
    register_email: ko.observable(),
    register_messages: ko.observableArray()
};

loginFormModel = {
    login_username: ko.observable(),
    login_password: ko.observable(),
    login_messages: ko.observableArray()
};
passwordRecoverModel = {
    pswd_recover_username: ko.observable(),
    pswd_recover_messages: ko.observableArray()
};

passwordChangeModel = {
    pswd_change_password: ko.observable(),
    pswd_change_passwordConfirm: ko.observable(),
    pswd_change_messages: ko.observableArray(),
    pswd_token: ko.observable()
};

authStatusModel = {
    loggedin: ko.observable(false)
};

$('#registerForm').submit(function (e) {
    e.preventDefault();
    if (registerFormModel.register_password() === registerFormModel.register_passwordConfirm()) {
        $.ajax({
            type: 'PUT',
            url: 'api/user_spa/account/' + registerFormModel.register_username(),
            data: JSON.stringify({
                password: registerFormModel.register_password(),
                email: registerFormModel.register_email(),
                autologin: true
            }),
            statusCode: {
                500: function () {
                    registerFormModel.register_messages(['Server error']);
                },
                200: function (response) {
                    registerFormModel.register_messages(response.messages);
                },
                201: function (response) {
                    registerFormModel.register_messages(response.messages);
                }
            }
        });
    } else {
        registerFormModel.register_messages(["Passwords don't match"]);
    }
});

$('#loginForm').submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/api/user_spa/account',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Basic ' + btoa(loginFormModel.login_username() + ':' + loginFormModel.login_password()));
        },
        statusCode: {
            500: function () {
                loginFormModel.login_messages(['Server error']);
            },
            200: function (response) {
                if (response.success === true) {
                    authStatusModel.loggedin(true);
                }
                loginFormModel.login_messages(response.messages);
            }
        }
    });
});

$('#passwordRecoveryForm').submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'api/user_spa/password/' + passwordRecoverModel.pswd_recover_username(),
        data: JSON.stringify({
            uid_type: 'username'
        }),
        statusCode: {
            500: function () {
                passwordRecoverModel.pswd_recover_messages(['Server error']);
            },
            200: function (response) {
                passwordRecoverModel.pswd_recover_messages(response.messages);
            }
        }
    });
});

$('#passwordChangeForm').submit(function (e) {
    e.preventDefault();
    if (passwordChangeModel.pswd_change_password() === passwordChangeModel.pswd_change_passwordConfirm()) {
        $.ajax({
            type: 'PUT',
            url: 'api/user_spa/password/' + user_id,
            data: JSON.stringify({
                password: passwordChangeModel.pswd_change_password(),
                token: $.url('?token'),
                autologin: true
            }),
            statusCode: {
                500: function () {
                    passwordChangeModel.pswd_change_messages(['Server error']);
                },
                200: function (response) {
                    toastr['success'](response.messages, 1000);
                    if (response.success === true) {
                        console.log('changed pswd successfully');
                        passwordChangeModel.pswd_change_password('');
                        passwordChangeModel.pswd_change_passwordConfirm('');
                    }
                }
            }
        });
    } else {
        passwordChangeModel.pswd_change_messages(["Passwords don't match"]);
    }
});

$(function () {

    ko.applyBindings(registerFormModel, document.getElementById('registerForm'));
    ko.applyBindings(loginFormModel, document.getElementById('loginForm'));
    ko.applyBindings(passwordRecoverModel, document.getElementById('passwordRecoveryForm'));
    ko.applyBindings(passwordChangeModel, document.getElementById('passwordChangeForm'));

    authStatusModel.loggedin.subscribe(function(status){
        if (status === true){
            $('#controls').hide();
        }
    })

    if ($.url('?token') != null) {

        passwordChangeModel.pswd_token($.url('?token'));
        $("#password_change_page").css("display", "block");

    }
})