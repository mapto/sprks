/*
Before any AJAX call, run statusUpdating().
In all AJAX callbacks, run statusReady().
 */

function statusUpdating(){
    statusBarModel.statusbar_image('static/img/ajax-loader.gif');
    statusBarModel.statusbar_status('Synchronising with server...')
}

function statusReady(){
    statusBarModel.statusbar_image('static/img/check.png');
    statusBarModel.statusbar_status('Synchronization complete. Ready.')
}

$(function(){
    statusBarModel.statusbar_image('static/img/check.png')
    statusBarModel.statusbar_status('Ready.')
})

function manage_toast_alert(text, delay){
    $("#toast").text(text);
    $("#toast").show();
    $('#toast').delay(delay).fadeOut();

}
