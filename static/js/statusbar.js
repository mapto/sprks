/*
Before any AJAX call, run statusUpdating().
In all AJAX callbacks, run statusReady().
 */

function statusUpdating(){
    formModel.statusbar_image('static/img/ajax-loader.gif');
    formModel.statusbar_status('Synchronising with server...')
}

function statusReady(){
    formModel.statusbar_image('static/img/check.png');
    formModel.statusbar_status('Synchronization complete. Ready.')
}

$(function(){
    formModel.statusbar_image('static/img/check.png')
    formModel.statusbar_status('Ready.')
})

function manage_toast_alert(text, delay){
    $("#toast").text(text);
    $("#toast").show();
    $('#toast').delay(delay).fadeOut();

}
