/*
Config and methods file for all notification/status management.

Before any AJAX call, run statusUpdating().
In all AJAX callbacks, run statusReady().
*/

toastr.options = {
  "debug": false,
  "positionClass": "toast-bottom-right",
  "onclick": toastr.clear(),
  "fadeIn": 300,
  "fadeOut": 1000,
  "timeOut": 2000,
  "extendedTimeOut": 3000
}

statusBarModel = {
    statusbar_status: ko.observable(),
    statusbar_image: ko.observable()
};

function statusUpdating() {
    statusBarModel.statusbar_image('static/img/ajax-loader.gif');
    statusBarModel.statusbar_status('Synchronising with server...')
}

function statusReady() {
    statusBarModel.statusbar_image('static/img/check.png');
    statusBarModel.statusbar_status('Synchronization complete. Ready.')
}

$(function () {

    ko.applyBindings(statusBarModel, document.getElementById('statusBar'));

    statusBarModel.statusbar_image('static/img/check.png')
    statusBarModel.statusbar_status('Ready.')
})
