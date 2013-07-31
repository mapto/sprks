registerFormModel = {
    username: ko.observable(),
    password: ko.observable(),
    passwordConfirm: ko.observable(),
    email: ko.observable(),
    messages: ko.observableArray()
};

loginModel = {
    username: ko.observable(),
    password: ko.observable(),
    messages: ko.observableArray(),
    loggedin: ko.observable(false)
};

passwordRecoverModel = {
    username: ko.observable(),
    messages: ko.observableArray()
};

passwordChangeModel = {
    password: ko.observable(),
    passwordConfirm: ko.observable(),
    messages: ko.observableArray(),
    token: ko.observable()
};

$('#registerForm').submit(function (e) {
    e.preventDefault();
    if (registerFormModel.password() === registerFormModel.passwordConfirm()) {
        $.ajax({
            type: 'PUT',
            url: 'api/user_spa/account/' + registerFormModel.username(),
            data: JSON.stringify({
                password: registerFormModel.password(),
                email: registerFormModel.email(),
                autologin: true
            }),
            statusCode: {
                500: function () {
                    registerFormModel.messages(['Server error']);
                },
                200: function (response) {
                    registerFormModel.messages(response.messages);
                },
                201: function (response) {
                    window.location='/';
                    registerFormModel.messages(response.messages);
                }
            }
        });
    } else {
        registerFormModel.messages(["Passwords don't match"]);
    }
});

$('#loginForm').submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/api/user_spa/account',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Basic ' + btoa(loginModel.username() + ':' + loginModel.password()));
        },
        statusCode: {
            500: function () {
                loginModel.messages(['Server error']);
            },
            200: function (response) {
                loginModel.messages(response.messages);
                if (response.success === true) {
                    loginModel.loggedin(true);
                    $('.main-body').hide();
                }
            }
        }
    });
});

$('#passwordRecoveryForm').submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'api/user_spa/password/' + passwordRecoverModel.username(),
        data: JSON.stringify({
            uid_type: 'username'
        }),
        statusCode: {
            500: function () {
                passwordRecoverModel.messages(['Server error']);
            },
            200: function (response) {
                passwordRecoverModel.messages(response.messages);
            }
        }
    });
});

$('#passwordChangeForm').submit(function (e) {
    e.preventDefault();
    if (passwordChangeModel.password() === passwordChangeModel.passwordConfirm()) {
        $.ajax({
            type: 'PUT',
            url: 'api/user_spa/password/' + user_id,
            data: JSON.stringify({
                password: passwordChangeModel.password(),
                token: $.url('?token'),
                autologin: true
            }),
            statusCode: {
                500: function () {
                    passwordChangeModel.messages(['Server error']);
                },
                200: function (response) {
                    toastr['success'](response.messages, 1000);
                    if (response.success === true) {
                        console.log('changed pswd successfully');
                        passwordChangeModel.password('');
                        passwordChangeModel.passwordConfirm('');
                    }
                }
            }
        });
    } else {
        passwordChangeModel.messages(["Passwords don't match"]);
    }
});

$('#logout-button').click(function(){
    $.ajax({
        type: 'GET',
        url: '/?action=logout',
        statusCode: {
            200: function () {
                    loginModel.loggedin(false);
                }
            }
    });
});

function check_loggedin() {
    $.ajax({
        type: 'POST',
        url: '/api/user_spa/account',
        statusCode: {
            200: function (response) {
                if (response.success === true) {
                    loginModel.loggedin(true);
                } else {
                    loginModel.loggedin(false);
                }
            }
        }
    });
}

$(function () {

    ko.applyBindings(registerFormModel, document.getElementById('registerForm'));
    ko.applyBindings(loginModel, document.getElementById('loginForm'));
    ko.applyBindings(passwordRecoverModel, document.getElementById('passwordRecoveryForm'));
    ko.applyBindings(passwordChangeModel, document.getElementById('passwordChangeForm'));

    loginModel.loggedin.subscribe(function(status){
        if (status === true){
            $('#controls').show();
            $('#logout-button').show();
            $('#login-button').hide();
        } else {
            $('#controls').hide();
            $('#logout-button').hide();
            $('#login-button').show();
        }
    })

    check_loggedin();

    if ($.url('?token') != null) {

        passwordChangeModel.token($.url('?token'));
        $("#password_change_page").css("display", "block");

    }
})