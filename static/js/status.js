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
  "timeOut": 3000,
  "extendedTimeOut": 3000
};

statusModel = {
    statusMessage: ko.observable('Ready.'),
    imagePath: ko.observable('static/img/check.png')
};

function statusUpdating() {
    statusModel.imagePath('static/img/ajax-loader.gif');
    statusModel.statusMessage('Synchronising with server...')
    $(".time_controls").addClass('disabled_controls');
}

function statusReady() {
    statusModel.imagePath('static/img/check.png');
    statusModel.statusMessage('Synchronization complete. Ready.')
    $(".time_controls").removeClass('disabled_controls');
}