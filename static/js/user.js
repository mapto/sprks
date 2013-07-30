function initUserForms(){

registerFormModel = {
        register_username: ko.observable(),
        register_password: ko.observable(),
        register_passwordConfirm: ko.observable(),
        register_email: ko.observable(),
        register_messages: ko.observableArray()
    };
ko.applyBindings(registerFormModel, document.getElementById('registerForm'));

passwordRecoverModel = {
        pswd_recover_username: ko.observable(),
        pswd_recover_messages: ko.observableArray()
    };
ko.applyBindings(passwordRecoverModel, document.getElementById('passwordRecoveryForm'));

loginFormModel = {
        login_username: ko.observable(),
        login_password: ko.observable(),
        login_messages: ko.observableArray()
    };
ko.applyBindings(loginFormModel, document.getElementById('loginForm'));

passwordChangeModel = {
        pswd_change_password: ko.observable(),
        pswd_change_passwordConfirm: ko.observable(),
        pswd_change_messages: ko.observableArray(),
        pswd_token: ko.observable()
    };
ko.applyBindings(passwordChangeModel, document.getElementById('passwordChangeForm'));

statusBarModel = {
        statusbar_status: ko.observable(),
        statusbar_image: ko.observable()
    };
ko.applyBindings(statusBarModel, document.getElementById('statusBar'));

intervieweeDeviceModel = {
        interviewee1_device_image: ko.observable(),
        interviewee2_device_image: ko.observable(),
        interviewee3_device_image: ko.observable()
    };
ko.applyBindings(intervieweeDeviceModel, document.getElementById('map'));

}

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
                    window.location = ("/");
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
                    manage_toast_alert(response.messages,1000);
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

    if ($.url('?token') != null) {

        passwordChangeModel.pswd_token($.url('?token'));
        $("#password_change_page").css("display", "block");

    }
})