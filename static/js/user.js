function initUserForms(){

    formModel = {
        register_username: ko.observable(),
        register_password: ko.observable(),
        register_passwordConfirm: ko.observable(),
        register_email: ko.observable(),
        register_messages: ko.observableArray(),
        login_username: ko.observable(),
        login_password: ko.observable(),
        login_messages: ko.observableArray(),
        pswd_recover_username: ko.observable(),
        pswd_recover_messages: ko.observableArray(),
        pswd_change_password: ko.observable(),
        pswd_change_passwordConfirm: ko.observable(),
        pswd_change_messages: ko.observableArray(),
        pswd_token: ko.observable(),
        statusbar_status: ko.observable(),
        statusbar_image: ko.observable(),
        interviewee1_device_image: ko.observable(),
        interviewee2_device_image: ko.observable(),
        interviewee3_device_image: ko.observable()
    };

    ko.applyBindings(formModel);

}

$('#registerForm').submit(function (e) {
    e.preventDefault();
    if (formModel.register_password() === formModel.register_passwordConfirm()) { // What is this? "==" means want to compare 2 string to be similar, not identical
        $.ajax({
            type: 'PUT',
            url: 'api/user_spa/account/' + formModel.register_username(),
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
            data: JSON.stringify({
                password: formModel.pswd_change_password(),
                token: $.url('?token'),
                autologin: true
            }),
            statusCode: {
                500: function () {
                    formModel.pswd_change_messages(['Server error']);
                },
                200: function (response) {
                    manage_toast_alert(response.messages,1000);
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



if ($.url('?token') != null) {

    formModel.pswd_token($.url('?token'));
    $("#password_change_page").css("display", "block");


}