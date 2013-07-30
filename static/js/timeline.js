/**
 * Created with PyCharm.
 * User: dkaliyev
 * Date: 30/07/2013
 * Time: 14:57
 * To change this template use File | Settings | File Templates.
 */
function setSyncDate() {
    window.first_date = new Date(window.date);
    window.nextSync = window.first_date;
    window.nextSync.setMonth(window.nextSync.getMonth()+1);
    window.nextSync.setDate(1);
    window.nextSyncStr = window.nextSync.getFullYear()+'-'+(window.nextSync.getMonth()+1)+'-'+window.nextSync.getDate();
    window.id_elem = 'plen';
}

function check_events() {
    var tmp_events_calendar = window.calendar;
    $(tmp_events_calendar).each(function(i) {
        var conv_date = new Date(tmp_events_calendar[i].date);
        var str_date = conv_date.getFullYear()+'-'+(conv_date.getMonth()+1)+'-'+conv_date.getDate();
        if(str_date == window.date)
        {
            $('#pause').click();
            tmp_event = tmp_events_calendar[i].events
            $(tmp_event).each(function(j){
                //alert("Event #"+tmp_event[j].incdt_id+" happend!");
                display_event(tmp_event[j].incdt_id, tmp_event[j].cost);
                submit_event(str_date);
            })
                $('.incident_page').click();

        }

    })

}


function submit_event(date){
        msg = {};
        msg['date'] = date;
        var request = $.ajax({
        url: "/api/chronos/event",
        type: "POST",
        // Async was false, but want to avoid perceived freeze on client side. Any risks, related to that?
        // E.g. what happens if the user changes screens too often
        async: true,
        data: JSON.stringify(msg),
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        success: function (response) {
            //
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
    }

function submit_change() { // need different event handling, to capture any change
    var msg = {
        date: time_parser($('#time').text()),
        policyUpdate: []
    };
    if(policyUpdate.length>0){
        msg.policyUpdate = policyUpdate;
        //msg.newCosts = calculate_cost_from_calendar();
    }
    msg.initPolicy = true;
    console.log(msg);
    statusUpdating();
    var request = $.ajax({
        url: "/api/chronos/update",
        type: "POST",
        data: JSON.stringify(msg),
        success: update_policy,
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}

function resume() {
    statusUpdating();
    var request = $.ajax({
        url: "/api/chronos/resume",
        type: "GET",
        success: function(policy) {
            policyUpdate = [];
            statusReady();
            console.log('response from server:' + policy);
            $('#pause').click();
            $('#time').text(time_visualiser(policy['date'], true));
            manageScoreButton();
            window.date = time_parser($('#time').text());
            window.calendar = policy['calendar'];
            setSyncDate();
            display_contextualized_policy(policy['policy'][0]);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}


startTimer = function (interval) {
        console.log("timer started");
        //window.open("/incident","_self")
        if (window.timer1 != null) pauseInterval();
        window.timer1 = setInterval(function () {
            //window.date = $('#time').text();
            var tmp = new Date(window.date);
            var addHours = 24;
            var addDays = 1;

            //tmp.setDate(tmp.getDate()+addDays);
            tmp.setHours(tmp.getHours()+addHours);

            var new_date = tmp.getFullYear()+'-'+(tmp.getMonth()+1)+'-'+tmp.getDate();

            var day_to_display = tmp.getDate(); if(day_to_display<10){day_to_display = '0'+day_to_display;}
            var month_to_display = tmp.getMonth()+1; if(month_to_display<10){month_to_display = '0'+month_to_display;}
            var date_to_display = tmp.getFullYear()+'-'+month_to_display+'-'+day_to_display;

            $('#time').text(time_visualiser(date_to_display, true));
            window.date = new_date;
            manageScoreButton();
            check_events();
            if(window.date==window.nextSyncStr) {
                manage_toast_alert("Changes submitted");
                $('#pause').click();
                window.first_date = new Date(window.date);
                window.nextSync = window.first_date;
                window.nextSync.setMonth(window.nextSync.getMonth()+2);
                window.nextSync.setDate(1);
                window.nextSyncStr = window.nextSync.getFullYear()+'-'+window.nextSync.getMonth()+'-'+window.nextSync.getDate();
                submit_change();
            }
            //script for interactive characters
            UpdateCharacters(time_parser($("#time").text())); //specified in characters.js

            },interval);
        return false;
}

pauseInterval = function() {
    clearInterval(window.timer1);
}