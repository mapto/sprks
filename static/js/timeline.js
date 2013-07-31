timelineModel = {
    currentDate: ko.observable(new Date(0))
};

function setSyncDate() {
    window.nextSync = new Date(timelineModel.currentDate());
    window.nextSync.setMonth(window.nextSync.getMonth() + 1);
    window.nextSync.setDate(1);
    window.id_elem = 'plen';
}

function check_events() {
    var tmp_events_calendar = window.calendar;
    $(tmp_events_calendar).each(function (i) {
        var conv_date = new Date(tmp_events_calendar[i].date);
        if (conv_date - timelineModel.currentDate() === 0) {
            $('#pause').click();
            tmp_event = tmp_events_calendar[i].events
            $(tmp_event).each(function (j) {
                display_event(tmp_event[j].incdt_id, tmp_event[j].cost);
                submit_event(str_date);
            })
            $('.incident_page').click();

        }
    })
}

function submit_event(date) {
    $.ajax({
        url: "/api/chronos/event",
        type: "POST",
        data: JSON.stringify({date: date}),
        success: function (response) {
            console.log("success: " + response.messages[0]);
        },
        error: function (response) {
            console.log("fail: " + response.messages[0]);
        }
    });
}

function submit_change() { // need different event handling, to capture any change
    var msg = {
        date: $.datepicker.formatDate($.datepicker.ISO_8601, timelineModel.currentDate()),
        policyUpdate: []
    };
    if (policyUpdate.length > 0) {
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
        success: function (policy) {
            policyUpdate = [];
            statusReady();
            $('#pause').click();
            timelineModel.currentDate($.datepicker.parseDate($.datepicker.ISO_8601, policy['date']))
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
    if (window.timer1 != null) pauseInterval();
    window.timer1 = setInterval(function () {
        var tmp = timelineModel.currentDate();

        tmp.setDate(tmp.getDate()+1);

        timelineModel.currentDate(tmp);

        check_events();
        if (timelineModel.currentDate() - window.nextSync === 0) {
            toastr['success']("Changes submitted");
            $('#pause').click();
            window.nextSync = new Date(timelineModel.currentDate());
            window.nextSync.setMonth(window.nextSync.getMonth() + 2);
            window.nextSync.setDate(1);

            submit_change();
        }
        //script for interactive characters
        UpdateCharacters($.datepicker.formatDate($.datepicker.ISO_8601, timelineModel.currentDate())); //specified in characters.js

    }, interval);
    return false;
}

pauseInterval = function () {
    clearInterval(window.timer1);
}

$(function () {
    ko.applyBindings(timelineModel, document.getElementById('timeline'));

    timelineModel.currentDate.subscribe(function () {
        if (timelineModel.currentDate - new Date('2014-2-1') < 0) {
            //console.log('less than 1 month passed. Score is not yet calculated, hide button');
            $(".score_page").css("display", "none");
        } else {
            //console.log('>=1 month passed. Score is calculated, show button.');
            $(".score_page").css("display", "block");
        }
        $(".incident_page").css("display", "none");
    })

})

function format_date(date) {
    return $.datepicker.formatDate($.datepicker.RFC_1123, date)
}